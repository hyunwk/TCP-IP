from socket import *
import threading

def send(sock):
    while True:
        msg = input()
        if not msg:
            continue
        try:
            sock.send(msg.encode())
        except:
            print("연결종료")
            break
    sock.close()

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                print("연결이 종료되었습니다.")
                break
            print(f'Received message: {msg.decode()}\n')
        except:
                print("연결이 종료되었습니다.")
                break
    sock.close()

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("localhost",2500))

    rThread = threading.Thread(target=send,args=(sock,))
    rThread.daemon = False
    rThread.start()
    sThread = threading.Thread(target=receive,args=(sock,))
    sThread.daemon = False
    sThread.start()
    
