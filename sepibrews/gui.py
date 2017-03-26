#!/usr/bin/env python
from __future__ import print_function, division
import os
import Tkinter as tk

class Sepis(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()
        self.master.bind('<Escape>', lambda e: self.quit())

    def makeWidgets(self):
        self.brew1 = Brew(self, padx=10, pady=5, ipadx=5, ipady=5)
        self.brew2 = Brew(self, padx=10, pady=5, ipadx=5, ipady=5)
        self.exitButton = ExitButton(self)

class Brew(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.recipeFrame = RecipeScrolledList(self, side=tk.LEFT,
                                            padx=10, pady=5, ipadx=5, ipady=5)
        self.buttonFrame = ButtonFrame(self, side=tk.LEFT, padx=10, pady=5, ipadx=5, ipady=5)
        self.timeFrame = TimeFrame(self, side=tk.LEFT, padx=10, pady=5, ipadx=5, ipady=5)
        self.tempFrame = TempFrame(self, side=tk.LEFT, padx=10, pady=5, ipadx=5, ipady=5)

class RecipeScrolledList(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.recipeList = tk.Listbox(self,
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

class ButtonFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.startButton = StartButton(self)
        self.stopButton = StopButton(self)

class StartButton(tk.Button):
    def __init__(self, parent=None, **options):
        tk.Button.__init__(self, parent)
        self.pack(**options)
        self.config(text='start')

class StopButton(tk.Button):
    def __init__(self, parent=None, **options):
        tk.Button.__init__(self, parent)
        self.pack(**options)
        self.config(text='stop')

class TimeFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.totalTimeLeftLabel = TotalTimeLeftLabel(self)
        self.stepTimeLeftLabel = StepTimeLeftLabel(self)

class TotalTimeLeftLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='total time left (min)')

class StepTimeLeftLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='step time left (min)')

class TempFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.pvLabel = PvLabel(self)
        self.svLabel = SvLabel(self)

class PvLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='pv: xx.xxC')

class SvLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='sv: xx.xxC')

class ExitButton(tk.Button):
    def __init__(self, parent=None, **options):
        tk.Button.__init__(self, parent)
        self.pack(**options)
        self.config(text='exit')

if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.option_add('*Font', 'DejaVuSans 20')
    myapp = Sepis(root)
    root.mainloop()
