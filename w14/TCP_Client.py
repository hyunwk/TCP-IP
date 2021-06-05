from socket import *

sock = socket()

svrIP = input(("server ip(default:127.0.0.1): "))
if svrIP == '':
    svrIP = '127.0.0.1'

port = input("port (default: 2500): ")
if port == '':
    port = 2500
else:
    port = int(port)

sock.connect((svrIP, port))
print("Connected to ", svrIP)

while True:
    msg = input("Sending message: ")
    
    if not msg:
        continue

    try:
        sock.send(msg.encode())
    except:
        print("connection closed")
        break

    try:
        msg = sock.recv(1024)
        if not msg:
            print("connection closed")
            break
        print("received message:", msg.decode())
    except:
        print("connection closed")
        break
sock.close()
