from Tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="Simple GUI")
        self.label.pack()

        self.label2 = Label(master, text="Some Text")

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.close_button = Button(master, text="Add New Label", command=self.addLabel)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

    def addLabel(self):
        self.label2.pack()

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()