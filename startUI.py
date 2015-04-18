import tkinter
import primes

class Application(tkinter.Frame):
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        self.chat = Chat(self)
        self.chat.grid(row = 0, column = 0)
        #self.setup = Setup(self)
        #self.setup.grid(row = 0, column =0)

class Chat(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self,master)
        self.createWidgets()

    def createWidgets(self):
        self.text = tkinter.Text(self)
        self.text.config(state=tkinter.DISABLED)
        self.text.grid(row =0, column = 0, rowspan = 2, columnspan=6)

        self.label = tkinter.Label(self,text="New Message: ")
        self.label.grid(row=2, column=0)
        
        self.entry = tkinter.Entry(self)
        self.entry.bind("<Key>", self.keyPress)
        self.entry.grid(row=2, column =1)
        
        self.button = tkinter.Button(self)
        self.button["text"] = "Display!"
        self.button["command"] = self.buttonClicked
        self.button.grid(row = 2, column=2)

        
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

        self.nLabel = tkinter.Label(self, text="n: ")
        self.nLabel.grid(row=2,column=0)
        
        self.nBox = tkinter.Entry(self)
        self.nBox.grid(row=2,column=1)
        self.nBox.insert(0,"23")

        self.gLabel = tkinter.Label(self, text="g: ")
        self.gLabel.grid(row=3, column=0)

        self.gBox = tkinter.Entry(self)
        self.gBox.grid(row=3, column=1)
        self.gBox.insert(0, "5")

        self.secretLabel = tkinter.Label(self, text="Secret Number:")
        self.secretLabel.grid(row=4, column=0)

        self.secretBox = tkinter.Entry(self)
        self.secretBox.grid(row=4, column=1)
        self.secretBox.insert(0, primes.randomSecret())

        
root = tkinter.Tk()
root.wm_title("TEST")
app = Application(master=root)
app.grid(row=0, column=0)
app.mainloop()
