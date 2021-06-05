from socket import *

port = 2500
address = ("localhost", port)
BUFSIZE = 1024

s = socket(AF_INET, SOCK_STREAM)
s.connect(address)

while True:
    msg = input("Message to send: ")
    s.send(msg.encode())

    if msg == 'a': 
        print("close client")
        break
    r_msg = s.recv(BUFSIZE)

    if not r_msg:
        break
    print("Received message", r_msg.decode())
