from socket import *
from threading import *

class MultiChatServer:
    clients = []
    final_recived_message = ""
    member_list = []
    #chat lists
    #messages = []


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
            print(ip,':',str(port),'socket:',c_socket,' 연결되었습니다.')
            t = Thread(target=self.receive_messages, args=(c_socket,))
            # add daemon
            t.daemon = False
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
                # get member name
                self.get_member(self.final_received_message)
                # insert message to messages
                #self.messages.insert(self.final_received_message)

                print(self.final_received_message) 
                #self.send_all_clients(c_socket)
                # fix to send socket and data
                self.send_all_clients(c_socket)
            c_socket.close()

    def send_all_clients(self, senders_socket):
        # add to constinusouly connect
        if "/q" == self.final_received_message:
            self.clients.remove(client)
            print(ip,port,"연결이 종료되었습니다.")
            return 

        for client in self.clients:
            socket, (ip,port) = client
            print('socket list :',socket)
            if socket is not senders_socket:
                try:
                    socket.sendall(self.final_received_message.encode('utf-8'))
                    print(socket,'socket success: ',self.final_received_message)
                except:
                    #self.clients.remove(client)
                    #print(ip,port,"연결이 종료되었습니다.")
                    pass
    
    def get_member(self,message):
        member = message[:message.find(":")-1]
        if member not in self.member_list:
            self.member_list.append(member)
            print("new member : ",member)

if __name__ == "__main__":
    MultiChatServer()
