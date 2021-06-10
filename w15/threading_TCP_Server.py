import socket
import threading

def handler(c,a):
    global connections
    while True:
        data = c.recv(1024)
        for connection in connections:
            connection.send(bytes(data))
        if not data:
            connections.remove(c)
            c.close()
            break
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("",2500))
sock.listen(5)
connections = []

while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(connections)
