import urllib.request
import socket

#encodedData = bytearray(urllib.parse.urlencode([("number",60)]),"utf-8")
#f = urllib.request.urlopen('http://127.0.0.1:8080/json',encodedData)
#print(f.read(1000))



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",25123))
s.send(b"HELLO SERVER, I am the client")
print(s.recv(4096).decode())

#s.send(b"GET / HTTP/1.0\n\n")
#data = s.recv(1024)
#print(data.decode())

