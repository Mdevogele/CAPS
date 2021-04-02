#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:26:23 2020

@author: maximedevogele
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:41:06 2019

@author: maximedevogele
"""

import os
import sys
print(sys.version_info[0])

if sys.version_info[0] == 3:
        # for Python2
    import tkinter as tk   ## notice capitalized T in Tkinter
    from tkinter import ttk
    from tkinter.filedialog import askopenfilenames
    from tkinter import messagebox
    # for Python3

else:
    # for Python2
    import tkinter as tk    ## notice lowercase 't' in tkinter here
    from tkinter import ttk
    from tkinter.filedialog import askopenfilenames
    from tkinter import messagebox

import __GUICONFIG__ as config
import GUI_toolbox as gtb
import Fits_display as fd

class SecondPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)

        frame_Menu = MenuBar(parent,self)
        frame_Menu.grid(row=0,column =0, sticky = "nsew")        
        
class MenuBar(tk.Frame):
    def __init__(self,parent, controller):
        
        tk.Frame.__init__(self,parent)

        Frame_Menu = tk.Frame(self,width=512,height=20)
        Frame_Menu.grid(row=0,column=0)
        
        mb = tk.Menubutton(Frame_Menu,text = "File")
        mb.menu = tk.Menu(mb)
        mb["menu"] = mb.menu
        
        mb.menu.add_command(label="Open fits files", command = lambda: fd.fits_display())
        
        mb.menu.add_command(label="Save settings", command = lambda: gtb.popupmsg("Not supported yet!"))        
        mb.menu.add_separator()
        mb.menu.add_command(label="Exit", command = quit)
        mb.grid(row=0,column =0)
        
        mb2 = tk.Menubutton(Frame_Menu,text = "Menu2")
        mb2.menu = tk.Menu(mb2)
        mb2["menu"] = mb2.menu
        
        mb2.menu.add_command(label="test1",command= lambda: popupmsg(str(self.winfo_width())))
        mb2.grid(row=0,column =1)

   
            