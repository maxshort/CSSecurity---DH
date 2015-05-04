import tkinter
import primes
import threading
import socket
import encrypt
import queue
import sys

class Application(tkinter.Frame):
    """Base of the application, can contain a setup window or a chat window"""
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        #self.chat = Chat(self)
        #self.chat.grid(row = 0, column = 0)
        self.setup = Setup(self, ("127.0.0.1",25123))
        self.setup.grid(row = 0, column =0)

    
class Chat(tkinter.Frame):
    """Chat interface. Has a box for chat history and a box/button to send new messages

       Attributes:
           soc (socket): a socket to communicate with other party
           encrypter(encryption class, optional): must have encrypt and decrypt methods (see encrypt.Vigenere or encrypt.Caesar) 
           master(tkinter.Frame): the frame within which to embed this frame
           messageQueue(queue): Queue where messages to be put on local ui are
              queued. Does not do networking. Messages should be formatted and
              decrypted before being placed in the message queue as the strings
              coming out of it are simply appended.
    """
    def __init__(self, soc, encrypter = None, master=None):
        """Initializes application window

        Args:
            soc (socket): a socket to communicate with other party
            encrypter(encryption class, optional): must have encrypt and decrypt methods (see encrypt.Vigenere or encrypt.Caesar) 
            master(tkinter.Frame, optional): the frame within which to embed this frame

        """
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
        """Initializes UI.

        Creates a box for message history, a box for new messages, a button
        for new messages and associated labels.

        """
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
        """Puts a message into the message Queue and also sends it over the network"""
        messageToSend = self.entry.get()
        if self.encrypter is not None:
            self.soc.send(bytearray(self.encrypter.encrypt(messageToSend), "utf-8"))
        self.messageQueue.put("You: " + messageToSend+"\n\n")
        self.entry.delete(0,tkinter.END)

    #Have  to run this on main thread.
    #Messages should be in plaintext by this point.
    def postMessages(self):
        """Reads from the message queue and posts the message

        Any formatting (e.g. names, new lines) should be done
        before entering messages into the messageQueue. Also,
        they should be decrypted at this point.
        """
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
        """Used to monitor for an enter press in the new message box.

        In the event of an enter press, it calls self.sendMessage()
        """
        c = event.char
        if c == "\r":
            self.sendMessage()

    def listenForMessages(self):
        """Listens from messages from other party over socket.
           When message is received, decrypts (if necessary), formats it and
           puts into self.messageQueue.
        """
        while True:
            messageFromOther = self.soc.recv(4096)
            messageFromOther = str(messageFromOther,"utf-8")
            if self.encrypter is not None:
                messageFromOther = self.encrypter.decrypt(messageFromOther)
            self.messageQueue.put("Them: " + messageFromOther + "\n\n")

            
class Setup(tkinter.Frame):
    """User interface for creating paramters for networked DH Vigenere key exchange

    Attributes:
        parent(Application, optional): usually the same as master. Frame within in which the chat window will be embeded.
        socketParams(tuple, optional): String address, int port
        master(Tkinter.Frame, optional): The Frame within which this is embedded.
    """
    #socketParams is a tuple of (addr, port) 
    def __init__(self, parent = None, socketParams=None, master=None):
        """Creates a Setup frame.

        Args:
            parent(Application, optional): usually the same as master. Frame within in which the chat window will be embeded.
            socketParams(tuple, optional): String address, int port
            master(Tkinter.Frame, optional): The Frame within which this is embedded.
        
        """
        tkinter.Frame.__init__(self,master)
        self.createWidgets()
        self.parent = parent
        self.socketParams = socketParams
        self.listeningSocket = socket.socket()
        self.listenerThread = threading.Thread(target=self.listenForConnections)
        self.listenerThread.setDaemon(True)
        self.listenerThread.start()
        
    def connectClicked(self):
        """Exchanges key with other party, changes UI to chat"""
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
        """Lays out setup UI"""
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
        """Listens for connections from another party.

           Upon connection exchanges keys and sets up chat window.
        """
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
        """Key press listener for address textbox.

           If enter is clicked it calls self.connectClicked.
        """
        c = event.char
        if c == "\r":
            self.connectClicked()
            
class EncryptionParams(tkinter.Frame):
    """Frame that holds a form for specifying parameters of DH/Vig key exchange

    Attributes:
        nBox(Entry): Value of n
        gBox(Entry): Value of g
        secretBox(Entry): Value of initial secret key
    """
    def __init__(self, master=None):
        """Creates EncryptionParams UI"""
        tkinter.Frame.__init__(self,master)
        self.config(bd=3,relief=tkinter.RIDGE)
        self.createWidgets()
        
    def createWidgets(self):
        """Lays out UI"""
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
