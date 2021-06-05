from socket import *

port = 2500
address = ("localhost", port)
BUFSIZE = 1024

s = socket()
s.connect(address)

while True:
    msg = input("Message to send: ")
    s.send(msg.encode())
    r_msg = s.recv(BUFSIZE)
    if not r_msg:
        break
    print("Received message : ", r_msg.decode())
