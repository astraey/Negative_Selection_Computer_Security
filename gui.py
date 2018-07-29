from Tkinter import Tk, Label, Button

class SystemGUI:
    def __init__(self, master):
        self.master = master

        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/2, height/2))

        master.title("Immune-Based Anomaly Detector")

        #self.label = Label(master, text="Simple GUI")
        #self.label.pack()

        self.label2 = Label(master, text="")

   


        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.close_button = Button(master, text="Add New Label", command=self.addLabel)
        self.close_button.pack()


    def greet(self):
        print("Greetings!")

    def addLabel(self):
        self.label2['text'] = "OOOOOOOOI"
        self.label2.pack()

    def changeMessage(self, message):
        self.label2['text'] = message
        self.label2.pack(side='bottom')

#root = Tk()
#my_gui = SystemGUI(root)
#root.mainloop()