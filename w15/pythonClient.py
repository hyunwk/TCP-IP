import socket

port = 2500
address = ("127.0.0.1", port)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
