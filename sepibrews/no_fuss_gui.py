#!/usr/bin/env python
from __future__ import print_function, division
import os
import Tkinter as tk
from no_fuss_statemachine import StateMachine

class Sepis(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()
        self.master.bind('<Escape>', lambda e: self.quit())

    def makeWidgets(self):
        self.brew1 = Brew(self, tempControllerAddress=1, padx=10, pady=5, ipadx=5, ipady=5)
        self.brew2 = Brew(self, tempControllerAddress=2, padx=10, pady=5, ipadx=5, ipady=5)
        self.exitButton = ExitButton(self)

class Brew(tk.Frame):
    def __init__(self, parent=None, tempControllerAddress=None, **options):
        tk.Frame.__init__(self, parent)
        self.sm = StateMachine(self, tempControllerAddress)
        self.pack(**options)
        self.makeWidgets()

    def destroy(self):
        self.sm.quit()
        tk.Frame.destroy(self)

    def makeWidgets(self):
        self.recipeFrame = RecipeScrolledList(self, side=tk.LEFT,
                                              padx=10, pady=5,
                                              ipadx=5, ipady=5)
        self.buttonFrame = ButtonFrame(self, side=tk.LEFT,
                                       padx=10, pady=5,
                                       ipadx=5, ipady=5)

    def getRecipe(self):
        return self.recipeFrame.getCurrentRecipe()

class RecipeScrolledList(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.recipeDirectory = './recipes'
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.recipeList = tk.Listbox(self,
                                     selectmode=tk.SINGLE,
                                     yscrollcommand=scrollbar.set,
                                     height=3,
                                     exportselection=False)
        scrollbar.config(command=self.recipeList.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipeList.pack(side=tk.TOP)
        for dirpath, dirnames, filenames in os.walk(self.recipeDirectory):
            for filename in sorted(filenames):
                if filename.endswith('.csv'):
                    self.recipeList.insert(tk.END, filename.split('.csv')[0])

    def getCurrentRecipe(self):
        return '{}/{}.csv'.format(self.recipeDirectory,
                                  self.recipeList.get('active'))

class ButtonFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.startButton = StartButton(self)

class StartButton(tk.Button):
    def __init__(self, parent=None, **options):
        self.parent = parent
        tk.Button.__init__(self, parent)
        self.pack(**options)
        self.config(text='start')
        self.config(command=self.parent.parent.sm.start)

class ExitButton(tk.Button):
    def __init__(self, parent=None, **options):
        tk.Button.__init__(self, parent)
        self.parent = parent
        self.pack(**options)
        self.config(text='exit')
        self.config(command=self.quit)

if __name__ == '__main__':
    root = tk.Tk()
    # root.attributes('-fullscreen', True)
    root.option_add('*Font', 'DejaVuSans 20')
    myapp = Sepis(root)
    root.mainloop()
    root.destroy()
