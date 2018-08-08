from Tkinter import Tk, Label, Button

class SystemGUI:
    def __init__(self, master):
        self.master = master

        self.storedTraining = False

        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/2, height/2))

        master.title("Immune-Based Anomaly Detector")

        self.label = Label(master, text="TRAINING STARTED")
        self.label['fg'] = '#2ac155'

        self.label3 = Label(master, text="")

        if self.storedTraining:
            self.label3['text'] = "STATUS: Training Stored"
        else:
            self.label3['text'] = "STATUS: Not trained"


        self.label3.pack()

        self.label2 = Label(master, text="")

        self.label4 = Label(master, text="")


    def addLabel(self):
        self.label2['text'] = ""
        self.label2.pack()

    def changeMessage(self, message):
        self.label2['text'] = message
        self.label2.pack(side='bottom')

    def startTraining(self):
        self.label['text'] = "TRAINING STARTED"
        self.label['fg'] = '#e0a204'
        self.label.pack()

    def changeStatusMessage(self, message):
        self.label3['text'] = message
        self.label3.pack()

    def changeErrorMessage(self, message, color):
        self.label4['text'] = message
        self.label4['fg'] = color
        self.label4.pack()