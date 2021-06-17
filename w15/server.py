from socket import *
from threading import *
import time
import json
class MultiChatServer:
    clients = []
    final_recived_message = ""
    member_dict = {}
    member_dict['dictionary_info'] = 'member'
    message_dict = {}
    message_dict['dictionary_info'] = 'message'
    message = {}

    def __init__(self):
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip =''
        self.port = 2500
        # so_reuseaddr = timewait 상태의 ip,port에  새로운 소켓 할당
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("waiting for clinets...")
        self.s_sock.listen(100)
        self.accept_client()

    def accept_client(self):
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)
            print(ip,':',str(port),' 연결되었습니다.')
            t = Thread(target=self.receive_messages, args=(c_socket,))
            t.start()

    def receive_messages(self, c_socket):
        while True:
            try:
                incoming_message = c_socket.recv(1024)
                if not incoming_message:
                    break
            except:
                continue
            else:
                self.final_received_message = incoming_message.decode("utf-8")

                # dict
                self.message_dict["message"] = self.final_received_message
                self.message['message'] = self.final_received_message

                self.get_member(c_socket, self.final_received_message)
                self.send_message_clients(c_socket)
                #self.send_member_clients(c_socket)
            # server quit 
            if "/q" == self.final_received_message.rstrip()[self.final_received_message.find(":")+2:]:
                c_socket.close()

    def send_message_clients(self, senders_socket):
        # add to constinusouly connect
        for client in self.clients:
            socket, (ip,port) = client
            try:
                print("send success")
                #message = json.dumps(self.message_dict).encode('utf-8')
                message = json.dumps(self.message).encode('utf-8')
                #socket.sendall(self.final_received_message.encode('utf-8'))
                socket.sendall(message)
            except:
                print("send fail")
                #self.clients.remove(client)
                #print(ip,port,"연결이 종료되었습니다.")
                pass
    
    def send_member_clients(self, senders_socket):
        # add to constinusouly connect
        for client in self.clients:
            socket, (ip,port) = client
            try:
                member = json.dumps(self.member_dict).encode('utf-8')
                socket.sendall(member)
            except:
                pass

    def get_member(self, sock, message):
        member = message[:message.find(":")-1]

#        if sock.getpeername()[1] in self.member_dict:
#            if self.member_dict[sock.getpeername()[1]] is not member:
#                self.member_dict[sock.getpeername()[1]] = member
#        else:
#            self.member_dict[sock.getpeername()[1]] = member
        print('port', sock.getpeername()[1])
        if sock.getpeername()[1] in self.message:
            if self.message[sock.getpeername()[1]] is not member:
                self.message[sock.getpeername()[1]] = member
        else:
            self.message[sock.getpeername()[1]] = member

if __name__ == "__main__":
    MultiChatServer()
