import tkinter
import primes
import threading
import socket
import encrypt
import queue
import sys

class Application(tkinter.Frame):
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        #self.chat = Chat(self)
        #self.chat.grid(row = 0, column = 0)
        self.setup = Setup(self, ("127.0.0.1",25123))
        self.setup.grid(row = 0, column =0)

    
class Chat(tkinter.Frame): 
    def __init__(self, soc, encrypter = None, master=None):
        tkinter.Frame.__init__(self,master)
        self.createWidgets()
        self.soc = soc
        self.encrypter = encrypter
        self.messageQueue = queue.Queue()
        
        self.listenerThread = threading.Thread(target=self.listenForMessages)
        self.listenerThread.daemon = True
        self.listenerThread.start()
        self.grid(row = 0, column=0)
        self.postMessages()

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
        self.button["command"] = self.sendMessage
        self.button.grid(row = 2, column=2)

    #posts own and sends over network    
    def sendMessage(self):
        messageToSend = self.entry.get()
        if self.encrypter is not None:
            self.soc.send(bytearray(self.encrypter.encrypt(messageToSend), "utf-8"))
        self.messageQueue.put("You: " + messageToSend+"\n\n")
        self.entry.delete(0,tkinter.END)

    #Have  to run this on main thread.
    #Messages should be in plaintext by this point.
    def postMessages(self):
        while True:
            try:
                self.update()
                message = self.messageQueue.get(False) 
                self.text.config(state = tkinter.NORMAL)
                self.text.insert(tkinter.END,message)
                self.text.config(state = tkinter.DISABLED)
            except queue.Empty:
                pass
            except: #most other exceptions mean that other client has closed
                self.soc.close()
                break
            
    
    def keyPress(self, event):
        c = event.char
        if c == "\r":
            self.sendMessage()

    def listenForMessages(self):
        while True:
            messageFromOther = self.soc.recv(4096)
            messageFromOther = str(messageFromOther,"utf-8")
            if self.encrypter is not None:
                messageFromOther = self.encrypter.decrypt(messageFromOther)
            self.messageQueue.put("Them: " + messageFromOther + "\n\n")

            
class Setup(tkinter.Frame):

    #socketParams is a tuple of (addr, port) 
    def __init__(self, parent = None, socketParams=None, master=None):
        tkinter.Frame.__init__(self,master)
        self.createWidgets()
        self.parent = parent
        self.socketParams = socketParams
        self.listeningSocket = socket.socket()
        self.listenerThread = threading.Thread(target=self.listenForConnections)
        self.listenerThread.setDaemon(True)
        self.listenerThread.start()
        
    def connectClicked(self):
        if self.parent is not None:
            
            soc = socket.socket()
            print("Address:"+self.urlBox.get().split(":")[0])
            print("Port: " + str(int(self.urlBox.get().split(":")[1])))
            soc.connect((self.urlBox.get().split(":")[0], int(self.urlBox.get().split(":")[1])))
            self.listeningSocket.close()
            secretKey = self.encryptionParams.secretBox.get()
            
            locksmith = encrypt.VigLocksmith(int(self.encryptionParams.gBox.get()), int(self.encryptionParams.nBox.get()),secretKey) 

            
            soc.send(bytearray(locksmith.makeIntermediateVal(), "utf-8"))
            otherKey = str(soc.recv(4096), "utf-8")
            print("KEY FROM OTHER: "+otherKey)
            finalKey = locksmith.makeKey(otherKey)
            print("FINAL KEY: "+finalKey)
            vi = encrypt.Vigenere((65,122), finalKey, False)
            
            self.parent.setup.grid_forget()
            self.parent.chat = Chat(soc, encrypter=vi, master=self.parent)


    def createWidgets(self):
        self.title = tkinter.Label(self, text = "New Connection")
        self.title.grid(row = 0,column=0, columnspan=2)

        self.encryptionParams = EncryptionParams(self)
        self.encryptionParams.grid(row=1, column=0, columnspan=2, pady=5)

        self.urlLabel = tkinter.Label(self,text = "URL Connection: ")
        self.urlLabel.grid(row=2, column=0)

        self.urlBox = tkinter.Entry(self)
        self.urlBox.grid(row=2, column=1)
        self.urlBox.bind("<Key>", self.keyPress)

        self.connectButton = tkinter.Button(self, text="Connect", command = self.connectClicked)
        self.connectButton.grid(row=3, column=1, sticky = tkinter.E)

    def listenForConnections(self):
        print("listening for connections")
        if self.socketParams is not None:
            try:
                self.listeningSocket.bind(self.socketParams)
                self.listeningSocket.listen(5)
                cliSoc, p = self.listeningSocket.accept()
                secretStr = self.encryptionParams.secretBox.get()
                locksmith = encrypt.VigLocksmith(int(self.encryptionParams.gBox.get()), int(self.encryptionParams.nBox.get()), secretStr)
                
                recKey = str(cliSoc.recv(4096), "utf-8")
                print("Key from other: " +recKey)
                vi = encrypt.Vigenere((65,122), locksmith.makeKey(recKey), False)

                cliSoc.send(bytearray(locksmith.makeIntermediateVal(),"utf-8"))
                
                self.grid_forget()
                self.parent.chat = Chat(cliSoc, encrypter = vi, master=self.parent)
            except OSError:
                #print("OS ERROR")
                raise #We will close the socket from elsewhere which will cause exception
            except:
                raise

    def keyPress(self, event):
        c = event.char
        if c == "\r":
            self.connectClicked()
            
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
        self.secretBox.insert(0, encrypt.genVigKey(5)) 

        
root = tkinter.Tk()
root.wm_title("Chat client")
app = Application(master=root)
app.grid(row=0, column=0)
app.mainloop()
