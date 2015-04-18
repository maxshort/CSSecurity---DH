import urllib.request

encodedData = bytearray(urllib.parse.urlencode([("number",60)]),"utf-8")
f = urllib.request.urlopen('http://127.0.0.1:8080/json',encodedData)
print(f.read(1000))
