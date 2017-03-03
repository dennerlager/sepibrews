#!/usr/bin/env python
from __future__ import print_function, division
import os
import Tkinter as tk

class Sepis():
    def __init__(self, parent):

        self.myParent = parent
        self.myParent.bind('<Escape>', lambda e: self.myParent.destroy())

        self.topFrame = tk.Frame(parent)
        self.topFrame.pack(expand=tk.YES, fill=tk.BOTH)

        self.brew1 = Brew(self.topFrame)
        self.brew1.pack(side=tk.TOP, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)

        self.brew2 = Brew(self.topFrame)
        self.brew2.pack(side=tk.TOP, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)

        self.util = tk.Frame(self.topFrame)
        self.util.pack(side=tk.TOP, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)

        self.exitButton = tk.Button(self.util, text='exit')
        self.exitButton.pack(side=tk.TOP)

class Brew(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.myParent = parent

        self.subframe1 = tk.Frame(self)
        self.subframe1.pack(side=tk.LEFT, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)
        self.subframe2 = tk.Frame(self)
        self.subframe2.pack(side=tk.LEFT, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)
        self.subframe3 = tk.Frame(self)
        self.subframe3.pack(side=tk.LEFT, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)
        self.subframe4 = tk.Frame(self)
        self.subframe4.pack(side=tk.LEFT, expand=tk.NO,  padx=10, pady=5, ipadx=5, ipady=5)

        self.recipeListFrame = tk.Frame(self.subframe1)
        self.recipeListFrame.pack(side=tk.TOP)
        scrollbar = tk.Scrollbar(self.recipeListFrame, orient=tk.VERTICAL)
        self.recipeList = tk.Listbox(self.recipeListFrame, 
                                     selectmode=tk.SINGLE, 
                                     yscrollcommand=scrollbar.set, 
                                     height=3)
        scrollbar.config(command=self.recipeList.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipeList.pack(side=tk.TOP)
        for dirpath, dirnames, filenames in os.walk('./recipes/'):
            for filename in sorted(filenames):
                if filename.endswith('.csv'):
                    self.recipeList.insert(tk.END, filename.split('.csv')[0])

        self.startButton = tk.Button(self.subframe2, text='start')
        self.startButton.pack(side=tk.TOP)

        self.stopButton = tk.Button(self.subframe2, text='stop')
        self.stopButton.pack(side=tk.TOP)

        self.totalTimeLeftLabel = tk.Label(self.subframe3, text='total time left: xxxmin')
        self.totalTimeLeftLabel.pack(side=tk.TOP)

        self.stepTimeLeftLabel = tk.Label(self.subframe3, text='step time left: xxxmin')
        self.stepTimeLeftLabel.pack(side=tk.TOP)

        self.pvLabel = tk.Label(self.subframe4, text='pv: xx.xC')
        self.pvLabel.pack(side=tk.TOP)

        self.svLabel = tk.Label(self.subframe4, text='sv: xx.xC')
        self.svLabel.pack(side=tk.TOP)

if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.option_add('*Font', 'DejaVuSans 20')
    # default_font = root.Font.nametofont('TkDefaultFont')
    # default_font.configure(size=48) 
    myapp = Sepis(root)
    root.mainloop()
