#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : provide a GUI for hang_man game, run the game from this 
    Start   : 09/28/2016
    End     : /2016
'''
# import hang_man
import random
from tkinter import *
from tkinter import ttk

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   # container for wedgets
         
        self.parent = parent # save a reference to the parent widget. 
        
        self.initUI() # creation of the user interface to the initUI() method
        
        self.centerWindow() # center the window
    
    def initUI(self):
      
        self.parent.title("Hang Man Game") #    set the title 
        self.pack(fill=BOTH, expand=1)
        self.style = Style()
        self.style.theme_use("default")
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=50, y=50)
        
    def centerWindow(self):
      
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        

def main():
    root = Tk() # root window is created, its a main application window in our programs. 
    app = Example(root) # instance of the application class.
    root.mainloop()   # event handling starts from this point


if __name__ == '__main__':
    main()
