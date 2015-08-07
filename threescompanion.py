#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from soundplayer import playSound
import soundlistener
from termcolor import colored, cprint

charKeyMap = {"'r'": "Red", "'b'": "Blue", "'w'": "White", "'p'": "Plus", "'i'": "Increment", "'z'": "Undo"}
baseBlocks = {"Red", "Blue", "White"}
colors = {"Red": "red", "Blue": "blue", "White": "white", "Played": "blue", "Unplayed": "grey", "Plus": "yellow", "Increment": "grey"}

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
        self.printState()
        playSound()
        
    def processKey(self, key):
        if (key in charKeyMap):
            self.processMove(charKeyMap[key])
    
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
                self.moves -= 1
            self.recordLast(key)
            
        elif key == "Undo":
            self.undo()
            
        self.printState()
            
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
        
        
    def printBaseBlocks(self):
        print "Upcoming base blocks:"
        blockCount = 0
        if self.incrementCount > 0: # We only show moves if all the blocks in this batch are known
            print str(12 - (self.colorCount % 12)) + " moves left in this batch\n"
            return
        
        for color in baseBlocks:
            for i in range(0, self.baseBlockCount[color]):
                printBlock(color)
                blockCount += 1
        print "\n"
                
    def printPlusBlocks(self):
        print "Plus block:"
        if self.moves < 21: # The first 21 moves have a grace period where no plus blocks appear
            print str(21 - self.moves) + " moves left in grace period\n"
            return
        
        offset = 0
        if self.foundPlus:
            offset = 1
                        
        for i in range (0, self.moves % 21 + offset):
            if self.foundPlus & ((i + 1) == self.lastPlus):
                printBlock("Plus")
            else:
                printBlock("Played")
        for i in range (self.moves % 21 + offset, 22):
            printBlock("Unplayed")
        print "\n"
            
    def printLastBlocks(self):
        print "Last blocks:"
        for i in range(0, len(self.lastMoves)):
            if self.lastMoves[i] == None:
                print "\n"
                return
            printBlock(self.lastMoves[i])
        print "\n"
    
    def printMoveCount(self):
        print "Move count: " + str(self.moves)
    
    def printState(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.printMoveCount()
        self.printLastBlocks()
        self.printBaseBlocks()
        self.printPlusBlocks()

def printBlock(block):
    cprint("  ", colors[block], "on_" + colors[block],end=''),
    print(" "),

def drawKeyboardShortcuts(window):
    window.create_text(560, 0, text="Red: r\nBlue: b\nWhite: w\nIncrement: i\nPlus block: p\nUndo: z", anchor="ne")

if __name__ == "__main__":
    game = Game()
    listener = soundlistener.SoundListener(game).listen()

    
    
    