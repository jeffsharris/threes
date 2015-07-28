#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk

class Game:
    def __init__(self):
        self.lastMoves = [None] * 4
        
        self.moves = 0
        self.colorCount = 8
        
        self.reds = 0
        self.blues = 0
        self.threes = 0
        
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
        if ((key == 'Red') | (key == 'Blue') | (key == 'Three')):
            self.colorCount += 1
            self.moves += 1
            if (key == 'Red'):
                self.reds += 1
            elif (key == 'Blue'):
                self.blues += 1
            else:
                self.threes += 1
            self.recordLast(key)
        elif (key == 'Plus'):
            self.foundplus = True
            self.recordLast(key)
        elif (key == 'Undo'):
            self.undo()
        
        
        
        if ((self.moves % 21 == 0) & (self.moves != 0)):
            self.foundplus = False
            
        if (self.colorCount % 12 == 0):
            self.reds = 0
            self.blues = 0
            self.threes = 0
            
    def undo(self):
        move = self.lastMoves[0]
        if ((move == 'Red') | (move == 'Blue') | (move == 'Three')):
            self.colorCount -= 1
            self.moves -= 1
            if (move == 'Red'):
                self.reds -= 1
            elif (move == 'Blue'):
                self.blues -= 1
            else:
                self.threes -= 1
        elif (move == 'Plus'):
            self.foundplus = False
        self.lastMoves.pop(0)
        self.lastMoves.append(None)
    
    def colorState(self):
        s = ""
        if(self.colorCount >= 12):
            s = "Reds: " + str(4 - self.reds) + "\n"
            s += "Blues: " + str(4 - self.blues) + "\n"
            s += "Threes: " + str(4 - self.threes) + "\n"
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
    if (event.char == 'r'):
        key = "Red"
    elif (event.char == 'b'):
        key = "Blue"
    elif (event.char == 't'):
        key = "Three"
    elif (event.char == 'p'):
        key = "Plus"
    elif (event.char == 'z'):
        key = "Undo"
    else:
        return
    game.processMove(key)
    text.delete(1.0, 'end')
    text.insert('end', '%s\n' % str(game))

game = Game()
root = tk.Tk()
root.geometry('350x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.wm_title("Threes Companion")
root.mainloop()