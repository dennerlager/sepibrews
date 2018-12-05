#!/usr/bin/env python3
import os
import tkinter as tk
from multiprocessing import Lock
from statemachine import StateMachine

class Sepis(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()
        self.master.bind('<Escape>', lambda e: self.quit())

    def makeWidgets(self):
        interfaceLock = Lock()
        self.brew1 = Brew(self, tempControllerAddress=1, interfaceLock=interfaceLock,
                          padx=10, pady=5, ipadx=5, ipady=5)
        self.brew2 = Brew(self, tempControllerAddress=2, interfaceLock=interfaceLock,
                          padx=10, pady=5, ipadx=5, ipady=5)
        self.exitButton = ExitButton(self)
        self.brew1.updateViews()
        self.brew2.updateViews()

class Brew(tk.Frame):
    def __init__(self, parent=None, tempControllerAddress=None,
                 interfaceLock=None, **options):
        tk.Frame.__init__(self, parent)
        self.tempControllerAddress = tempControllerAddress
        self.sm = StateMachine(self, tempControllerAddress, interfaceLock)
        self.pack(**options)
        self.makeWidgets()

    def destroy(self):
        self.sm.quit()
        tk.Frame.destroy(self)

    def makeWidgets(self):
        self.brewLabel = BrewLabel(self, brewLabelText=self.tempControllerAddress,
                                   side=tk.TOP,
                                   padx=10, pady=0,
                                   ipadx=5, ipady=5,
                                   anchor='w')
        self.recipeFrame = RecipeScrolledList(self, side=tk.LEFT,
                                              padx=10, pady=5,
                                              ipadx=5, ipady=5)
        self.buttonFrame = ButtonFrame(self, side=tk.LEFT,
                                       padx=10, pady=5,
                                       ipadx=5, ipady=5)
        self.timeFrame = TimeFrame(self, side=tk.LEFT,
                                   padx=10, pady=5,
                                   ipadx=5, ipady=5)
        self.tempFrame = TempFrame(self, side=tk.LEFT,
                                   padx=10, pady=5,
                                   ipadx=5, ipady=5)

    def updateViews(self):
        self.sm.updateViews()
        self.after(500, self.updateViews)

    def getRecipe(self):
        return self.recipeFrame.getCurrentRecipe()

    def getStateMachine(self):
        return self.sm

    def setProcessValue(self, pv):
        self.tempFrame.setProcessValue(pv)

    def setSetValue(self, sv):
        self.tempFrame.setSetValue(sv)

    def setStepTimeLeft(self, stl):
        self.timeFrame.setStepTimeLeft(stl)

    def setTotalTimeLeft(self, ttl):
        self.timeFrame.setTotalTimeLeft(ttl)

class BrewLabel(tk.Label):
    def __init__(self, parent=None, brewLabelText=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='Sud {}'.format(brewLabelText))

class RecipeScrolledList(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        path = os.path.dirname(os.path.realpath(__file__))
        self.recipeDirectory = path + '/recipes'
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.recipeList = tk.Listbox(self,
                                     selectmode=tk.SINGLE,
                                     yscrollcommand=scrollbar.set,
                                     height=3,
                                     width = 14,
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
        self.stopButton = StopButton(self)

    def getStateMachine(self):
        return self.parent.getStateMachine()

class StartButton(tk.Button):
    def __init__(self, parent=None, **options):
        self.parent = parent
        tk.Button.__init__(self, parent)
        self.pack(**options)
        self.config(text='start')
        self.config(command=self.getStateMachine().start)

    def getStateMachine(self):
        return self.parent.getStateMachine()

class StopButton(tk.Button):
    def __init__(self, parent=None, **options):
        tk.Button.__init__(self, parent)
        self.parent = parent
        self.pack(**options)
        self.config(text='stop')
        self.config(command=self.getStateMachine().stop)

    def getStateMachine(self):
        return self.parent.getStateMachine()

class TimeFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.totalTimeLeftLabel = TotalTimeLeftLabel(self)
        self.stepTimeLeftLabel = StepTimeLeftLabel(self)

    def setStepTimeLeft(self, stl):
        self.stepTimeLeftLabel.setStepTimeLeft(stl)

    def setTotalTimeLeft(self, ttl):
        self.totalTimeLeftLabel.setTotalTimeLeft(ttl)

class TotalTimeLeftLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='Total xxmin')

    def setTotalTimeLeft(self, ttl):
        self.config(text='Total {:.1f}min'.format(ttl/60))

class StepTimeLeftLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='Schritt xxmin')

    def setStepTimeLeft(self, stl):
        self.config(text='Schritt {:.1f}min'.format(stl/60))

class TempFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.pvLabel = PvLabel(self)
        self.svLabel = SvLabel(self)

    def setProcessValue(self, pv):
        self.pvLabel.setProcessValue(pv)

    def setSetValue(self, sv):
        self.svLabel.setSetValue(sv)

class PvLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='pv: xx.xxC')

    def setProcessValue(self, pv):
        self.config(text='pv: {:.1f}C'.format(pv))

class SvLabel(tk.Label):
    def __init__(self, parent=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='sv: xx.xxC')

    def setSetValue(self, sv):
        self.config(text='sv: {:.1f}C'.format(sv))

class ExitButton(tk.Button):
    def __init__(self, parent=None, **options):
        tk.Button.__init__(self, parent)
        self.parent = parent
        self.pack(**options)
        self.config(text='exit')
        self.config(command=self.quit)

if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.option_add('*Font', 'DejaVuSans 20')
    myapp = Sepis(root)
    # root.wm_maxsize(800, 480)
    # root.wm_minsize(800, 480)
    root.mainloop()
    root.destroy()
