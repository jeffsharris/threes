#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk

charKeyMap = {"r": "Red", "b": "Blue", "t": "Three", "p": "Plus", "z": "Undo"}
baseBlocks = {"Red", "Blue", "Three"}

class Game:
    def __init__(self):
        self.lastMoves = [None] * 4
        
        self.moves = 0
        self.colorCount = 8
        
        self.baseBlockCount = {"Red": 0, "Blue": 0, "Three": 0};
        
        self.foundplus = True
        
    def __str__(self):
         s = "Last four moves: " + str(self.lastMoves) + "\n"
         s += self.colorState()
         s += self.plusState()
         return s
        
    def recordLast(self, value):
        self.lastMoves.insert(0, value)
        self.lastMoves.pop()
         
    def processMove(self, key):
        if (key in baseBlocks):
            self.colorCount += 1
            self.moves += 1
            self.baseBlockCount[key] += 1
            self.recordLast(key)
        elif (key == "Plus"):
            self.foundplus = True
            self.recordLast(key)
        elif (key == "Undo"):
            self.undo() 
        
        if ((self.moves % 21 == 0) & (self.moves != 0)):
            self.foundplus = False
            
        if (self.colorCount % 12 == 0):
            self.baseBlockCount = {"Red": 0, "Blue": 0, "Three": 0};
            
    def undo(self):
        move = self.lastMoves[0]
        if (move in baseBlocks):
            self.colorCount -= 1
            self.moves -= 1
            self.baseBlockCount[move] -= 1
        elif (move == "Plus"):
            self.foundplus = False
        self.lastMoves.pop(0)
        self.lastMoves.append(None)
    
    def colorState(self):
        s = ""
        if(self.colorCount >= 12):
            for color, count in self.baseBlockCount.items():
                s += color + ": " + str(4 - count) + "\n"
        else:
            s = "Red/Blue/Threes depend on starting position\n"
        return s
        
    
    def plusState(self):
        if (self.foundplus == True):
            s = "The next " + str(21 - (self.moves % 21)) + " moves don't have plus blocks\n"
        else:
            s = "A plus block is coming in the next " + str(21 - (self.moves % 21)) + " moves\n" 
        return s
    

def onKeyPress(event):
    if (event.char in charKeyMap):
        game.processMove(charKeyMap[event.char])
        text.delete(1.0, "end")
        text.insert("end", "%s\n" % str(game))

game = Game()
root = tk.Tk()
root.geometry("350x200")
text = tk.Text(root, background="black", foreground="white", font=("Comic Sans MS", 12))
text.pack()
root.bind("<KeyPress>", onKeyPress)
root.wm_title("Threes Companion")
root.mainloop()