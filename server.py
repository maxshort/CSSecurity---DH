#Accepting server

import socket
import threading

class ConnectionHandler(threading.Thread):
    def __init__(self, socket):
        """socket is the connection to the client. this ConnectionHandler will close it"""
        super().__init__()
        self.socket = socket

    def run(self):
        print("I RAN")
        print(self.socket.recv(4096).decode())
        self.socket.send(b"well hello client")
        self.socket.close()    

s = socket.socket()
host = "127.0.0.1" #local machine
port = 25000
s.bind((host,port))

s.listen(5)

while True:
    soc, addr = s.accept()
    conHand = ConnectionHandler(soc)
    conHand.start()
    



#EACH CLIENT HAS TWO THREADS...1 listener thread and one ui thread
