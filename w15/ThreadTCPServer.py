import socket
import _thread

BUFF = 1024
HOST = '127.0.0.1'
PORT = 2500

def response(key):
    return '서버 응답 메시지'

def handler(clientsock, addr):
    while True:
        data = clientsock.recv(BUFF)
        if not data:
            break
        clientsock.send(response('').encode())
        print('sent:', repr(response('')))

if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)

    while True:
        print("waiting for connection")
        clientsock, addr = serversock.accept()
        print("...connected from:",addr)
        _thread.start_new_thread(handler, (clientsock,addr))
