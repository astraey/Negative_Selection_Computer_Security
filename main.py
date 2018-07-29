#!/usr/bin/env python
 
from subprocess import Popen, PIPE
from re import split
from sys import stdout
import utils as utils
from Tkinter import Tk, Label, Button
from gui import SystemGUI

from process import Proc


root = Tk()
my_gui = SystemGUI(root)
#root.mainloop()
root.update_idletasks()
root.update()

utils.mainScript(my_gui, root)