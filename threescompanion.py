#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import os
import multiprocessing
from soundplayer import playSound
import soundlistener

charKeyMap = {"r": "Red", "b": "Blue", "w": "White", "p": "Plus", "i": "Increment", "z": "Undo"}
baseBlocks = {"Red", "Blue", "White"}
colors = {"Red": "#FF6780", "Blue": "#66CBFF", "White": "#F8F8F8", "Played": "#111111", "Unplayed": "#EEEEEE", "Plus": "#FBCC67", "Increment": "#999999"}

class Game:
    def __init__(self):
        self.lastMoves = [None] * 12 # Record the most recent moves for display and to support undo. Limit of 4 undos.
        self.moves = 0
        
        self.colorCount = 8 # Track how many color blocks have been played in this batch. Important because the board starts with 8 blocks
        self.resetColors()
        self.incrementCount = 8 # Count the number of times we've incremented the move count in this batch without recording the color
        
        self.foundPlus = False # Whether we've already seen a plus block in this batch of 21
        self.lastPlus = 0 # The index of the most recent plus block
        
    def recordLast(self, value):
        if (self.lastMoves[0] != "Increment") | (self.incrementCount == 0): # Only record the specific move if it hasn't already been recorded and if the batch
            return False
        self.lastMoves[0] = value
        self.incrementCount -= 1
        return True
        
    def resetColors(self):
        self.baseBlockCount = {"Red": 4, "Blue": 4, "White": 4}
    
    def processIncrement(self):
        self.lastMoves.insert(0, "Increment")
        self.lastMoves.pop()
        
        self.incrementCount += 1
        self.incrementBaseBlocks()
        playSound()
    
    def processMove(self, key):
        if key in baseBlocks:
            if self.baseBlockCount[key] == 0: # Invalid input, you've found more than 4 of this block in this batch
                return
            
            if self.recordLast(key): # We successfully replaced the last incremented move with the specific block
                self.baseBlockCount[key] -= 1
                self.lastMoves[0] = key
            
        elif key == "Increment":            
            self.processIncrement()
            
        elif key == "Plus":
            if self.recordLast(key):
                self.foundPlus = True
                self.lastPlus = self.moves % 21
            self.recordLast(key)
            
        elif key == "Undo":
            self.undo()
            
    def incrementBaseBlocks(self):
        self.moves += 1
        self.colorCount += 1
        if self.moves % 21 == 0: # Entering a new batch of plus blocks
            self.foundPlus = False
        if (self.colorCount % 12 == 0): # Entering a new batch of color blocks
            self.resetColors()
            self.incrementCount = 0
    
    def undo(self):
        move = self.lastMoves[0]
        if (move in baseBlocks) | (move == "Plus"):
            self.lastMoves[0] = "Increment"
            self.incrementCount += 1
            if move in baseBlocks:
                self.baseBlockCount[move] = self.baseBlockCount[move] + 1
            else:
                foundPlus = False
        elif move == "Increment":
            self.colorCount -= 1
            self.moves -= 1
            if self.moves % 21 == 20:
                self.foundPlus = True 
            if self.colorCount % 12 == 0:
                self.resetColors()
            self.incrementCount -= 1
            self.lastMoves.pop(0)
            self.lastMoves.append(None)
        
        
    def drawBaseBlocks(self, window, y):
        window.create_text(10, y, text="Upcoming base blocks:", anchor="nw")
        blockCount = 0
        if self.incrementCount > 0: # We only show moves if all the blocks in this batch are known
            s = str(12 - (self.colorCount % 12)) + " moves left in this batch"
            window.create_text(10, y+20, text=s, anchor="nw")
            return
        
        for color in baseBlocks:
            for i in range(0, self.baseBlockCount[color]):
                drawBlock(window, 10 + 25*blockCount, y + 20, color)
                blockCount += 1
                
    def drawPlusBlocks(self, window, y):
        window.create_text(10, y, text="Plus block:", anchor="nw")
        if self.moves < 21: # The first 21 moves have a grace period where no plus blocks appear
            s = str(21 - self.moves) + " moves left in grace period"
            window.create_text(10, y+20, text=s, anchor="nw")
            return
        
        offset = 0
        if self.foundPlus:
            offset = 1
                        
        for i in range (0, self.moves % 21 + offset):
            drawBlock(window, 10 + 25 * i, y + 20, "Played")
        for i in range (self.moves % 21 + offset, 22):
            drawBlock(window, 10 + 25 * i, y + 20, "Unplayed")
        
        if self.foundPlus:
            drawBlock(window, 10 + 25 * self.lastPlus, y + 20, "Plus")
            
    def drawLastBlocks(self, window, y):
        window.create_text(10, y, text="Last blocks:", anchor="nw")
        for i in range(0, len(self.lastMoves)):
            if self.lastMoves[i] == None:
                return
            drawBlock(window, 10 + 25 * i, y + 20, self.lastMoves[i])
    
    def drawMoveCount(self, window, y):
        s = "Move count: " + str(self.moves)
        window.create_text(10, y, text=s, anchor="nw")
    
    def drawState(self, window):
        self.drawMoveCount(window, 10)
        self.drawLastBlocks(window, 30)
        self.drawBaseBlocks(window, 110)
        self.drawPlusBlocks(window, 190)

def drawBlock(window, x, y, block):
    window.create_rectangle(x, y, x + 20, y + 40, fill=colors[block])

def drawKeyboardShortcuts(window):
    window.create_text(560, 0, text="Red: r\nBlue: b\nWhite: w\nIncrement: i\nPlus block: p\nUndo: z", anchor="ne")

class Window:
    def __init__(self, game):
        self.game = game
        self.root = Tk()
        self.window = Canvas(self.root, width=570, height=290)
        self.window.pack()
        self.root.bind("<KeyPress>", self.onKeyPress)
        self.root.wm_title("Threes Companion")
        drawKeyboardShortcuts(self.window)

    def onKeyPress(self, event):
        if (event.char in charKeyMap):
            self.window.delete("all")
            self.game.processMove(charKeyMap[event.char])
            self.game.drawState(self.window)
        drawKeyboardShortcuts(self.window)

    def start(self):
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        self.root.mainloop()
        print "Finished"

if __name__ == "__main__":
    game = Game()
    
    multiprocessing.Process(target=soundlistener.start,args=[game]).start()
    
    window = Window(game).start()

    
    
    