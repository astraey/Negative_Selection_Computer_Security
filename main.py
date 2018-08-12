from Tkinter import Tk, Label, Button
from gui import SystemGUI
import utils as utils

# Initialisation of the GUI
root = Tk()
my_gui = SystemGUI(root)
root.update_idletasks()
root.update()

# Main script execution
utils.mainScript(my_gui, root)