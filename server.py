#Accepting server

import socket

s = socket.socket()
host = socket.gethostname() #local machine
port = 15000
s.bind((host,port))

s.listen(5) #listen for 5 seconds?

while True:
    c, addr = s.accept()
    print ("Got connection from " + str(addr))
    c.close()
