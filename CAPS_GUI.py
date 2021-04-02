#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:15:13 2020

@author: maximedevogele
"""

from tkinter import *
from tkinter import ttk
#from tkinter.filedialog import askopenfilename
#from tkinter.filedialog import askopenfilenames
#from tkinter.messagebox import showerror
from tkinter import messagebox



class simpleapp_tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        
        # Closing handeler
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)    



        # Definition of the frame containing the processing tabs
        self.frame_process=Frame(self, width=200, height=800)
        self.frame_process.grid(column=0, row=0)
        self.frame_Images=Frame(self, width=800, height=800)
        self.frame_Images.grid(column=1, row=0)

        self.CBias_button = Button(self.frame_process, text="Create Biases")
        self.CBias_button.grid(row=0, column=0)
#        self.CBias_button.bind("<ButtonRelease-1>", self.load_file)         



    # Closing command 
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
#            self.f.close()
            self.quit()
            self.destroy()


if __name__ == "__main__":
    
    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('CAPS Pipeline')

    # start Tk
    app.mainloop()