from Tkinter import Tk, Label, Button

class SystemGUI:
    def __init__(self, master):
        self.master = master

        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/2, height/2))

        master.title("Immune-Based Anomaly Detector")

        self.label = Label(master, text="READY")
        self.label['fg'] = '#2ac155'
        self.label.pack()

        self.label3 = Label(master, text="READY")
        self.label3.pack()

        self.storedTraining = False

        self.label2 = Label(master, text="")

   
        self.start_button = Button(master, text="Start Training", command=self.startTraining)
        self.start_button.pack()


        #self.close_button = Button(master, text="Close", command=master.quit)
        #self.close_button.pack()

    def addLabel(self):
        self.label2['text'] = "OOOOOOOOI"
        self.label2.pack()

    def changeMessage(self, message):
        self.label2['text'] = message
        self.label2.pack(side='bottom')

    def startTraining(self):
        self.label['text'] = "TRAINING STARTED"
        self.label['fg'] = '#bfc12a'
        self.label.pack()

#root = Tk()
#my_gui = SystemGUI(root)
#root.mainloop()