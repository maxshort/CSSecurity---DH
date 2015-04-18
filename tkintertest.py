import tkinter

class Application(tkinter.Frame):
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        #self.chat = Chat(self)
        self.setup = Setup(self)
        self.setup.grid(row = 0, column =0)

class Chat(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.text = tkinter.Text(self)
        self.text.config(state=tkinter.DISABLED)
        self.text.pack()

        self.label = tkinter.Label(self,text="New Message: ")
        self.label.pack(side="left")
        
        self.entry = tkinter.Entry(self)
        self.entry.bind("<Key>", self.keyPress)
        self.entry.pack(side = "left")
        
        self.button = tkinter.Button(self)
        self.button["text"] = "Display!"
        self.button["command"] = self.buttonClicked
        self.button.pack(side="left")

        
    def buttonClicked(self):
        self.text.config(state = tkinter.NORMAL)
        self.text.insert(tkinter.END,self.entry.get()+"\n")
        self.text.config(state = tkinter.DISABLED)
        self.entry.delete(0,tkinter.END)

    def keyPress(self, event):
        c = event.char
        if c == "\r":
            self.buttonClicked()

class Setup(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self,master)
        self.createWidgets()
    def createWidgets(self):
        self.title = tkinter.Label(self, text = "New Connection")
        self.title.grid(row = 0,column=0, columnspan=2)

        self.encryptionParams = EncryptionParams(self)
        self.encryptionParams.grid(row=1, column=0, columnspan=2, pady=5)

        self.urlLabel = tkinter.Label(self,text = "URL Connection: ")
        self.urlLabel.grid(row=2, column=0)

        self.urlBox = tkinter.Entry(self)
        self.urlBox.grid(row=2, column=1)

        self.connectButton = tkinter.Button(self, text="Connect")
        self.connectButton.grid(row=3, column=1, sticky = tkinter.E)

class EncryptionParams(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self,master)
        self.config(bd=3,relief=tkinter.RIDGE)
        self.createWidgets()
        
    def createWidgets(self):
        self.title = tkinter.Label(self, text = "Encryption Parameters")
        self.title.grid(row=0, columnspan =2,sticky = tkinter.E+tkinter.W)
        
        self.autoGenButton = tkinter.Button(self)
        self.autoGenButton["text"] = "Auto Generate"
        self.autoGenButton.grid(row=1)

        self.nLabel = tkinter.Label(self, text="n: ")
        self.nLabel.grid(row=2,column=0)
        
        self.nBox = tkinter.Entry(self)
        self.nBox.grid(row=2,column=1)

        self.gLabel = tkinter.Label(self, text="g: ")
        self.gLabel.grid(row=3, column=0)

        self.gBox = tkinter.Entry(self)
        self.gBox.grid(row=3, column=1)

        self.secretLabel = tkinter.Label(self, text="Secret Number:")
        self.secretLabel.grid(row=4, column=0)

        self.secretBox = tkinter.Entry(self)
        self.secretBox.grid(row=4, column=1)

        
root = tkinter.Tk()
root.wm_title("TEST")
app = Application(master=root)
app.grid(row=0, column=0)
app.mainloop()
