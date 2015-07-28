#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import os

charKeyMap = {"r": "Red", "b": "Blue", "w": "White", "p": "Plus", "z": "Undo"}
baseBlocks = {"Red", "Blue", "White"}
colors = {"Red": "#FF6780", "Blue": "#66CBFF", "White": "#F8F8F8", "Played": "#111111", "Unplayed": "#EEEEEE", "Plus": "#FBCC67"}

class Game:
    def __init__(self):
        self.lastMoves = [None] * 4 # Record the most recent moves for display and to support undo. Limit of 4 undos.
        
        self.moves = 0
        self.colorCount = 8 # Track how many color blocks have been played in this batch. Important because the board starts with 8 blocks
        
        self.baseBlockCount = {"Red": 4, "Blue": 4, "White": 4}; #Initialize to 0 because some blocks are already populated on screen
        
        self.foundPlus = False # Whether we've already seen a plus block in this batch of 21
        self.lastPlus = 0 # The index of the most recent plus block
        
    def recordLast(self, value):
        self.lastMoves.insert(0, value)
        self.lastMoves.pop()
         
    def processMove(self, key):
        if key in baseBlocks:
            if self.baseBlockCount[key] == 0: # Invalid input, you've found more than 4 of this block in this batch
                return
            self.colorCount += 1
            self.moves += 1
            self.baseBlockCount[key] -= 1
            self.recordLast(key)
            
            if self.moves % 21 == 0: # Entering a new batch of plus blocks
                self.foundPlus = False
            if (self.colorCount % 12 == 0): # Entering a new batch of color blocks
                self.baseBlockCount = {"Red": 4, "Blue": 4, "White": 4};
        elif key == "Plus":
            self.foundPlus = True
            self.lastPlus = self.moves % 21
            self.recordLast(key)
        elif key == "Undo":
            self.undo()          
            
    def undo(self):
        move = self.lastMoves[0]
        if (move in baseBlocks):
            self.colorCount -= 1
            self.moves -= 1
            self.baseBlockCount[move] = self.baseBlockCount[move] + 1
            if self.moves % 21 == 20:
                self.foundPlus = True
        elif (move == "Plus"):
            self.foundPlus = False
        self.lastMoves.pop(0)
        self.lastMoves.append(None)
        
    def drawBaseBlocks(self, window, y):
        window.create_text(10, y, text="Upcoming base blocks:", anchor="nw")
        blockCount = 0
        if self.moves < 4: # We don't count blocks until you enter the first full batch of base blocks (after move 12)
            s = str(12 - self.colorCount) + " moves left in this batch"
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
    
    def drawState(self, window):
        self.drawLastBlocks(window, 0)
        self.drawBaseBlocks(window, 80)
        self.drawPlusBlocks(window, 160)

def drawBlock(window, x, y, block):
    window.create_rectangle(x, y, x + 20, y + 40, fill=colors[block])

def drawKeyboardShortcuts(window):
    window.create_text(560, 0, text="Red: r\nBlue: b\nWhite: w\nPlus block: p\nUndo: z", anchor="ne")

def onKeyPress(event):
    if (event.char in charKeyMap):
        window.delete("all")
        game.processMove(charKeyMap[event.char])
        game.drawState(window)
    drawKeyboardShortcuts(window)

game = Game()
root = Tk()

window = Canvas(root, width=570, height=250)
window.pack()

root.bind("<KeyPress>", onKeyPress)
root.wm_title("Threes Companion")
drawKeyboardShortcuts(window)
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
root.mainloop()