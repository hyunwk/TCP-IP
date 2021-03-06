from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *
import time
import json

class ChatClient:
    client_socket = None
    close_flag = False

    def __init__(self, ip, port):
        self.initialize_socket(ip,port)
        self.initialize_gui()
        self.listen_thread()

    def initialize_socket(self, ip, port):
        # tcp socket 생성, server 연결
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):
        # message 전송하는 callback 함수
        self.root = Tk()
        fr=  []
        for i in range(7):
            fr.append(Frame(self.root))
            fr[i].pack(fill=BOTH)
            
        self.name_label = Label(fr[0], text=' 사용자이름')
        self.quit_btn = Button(fr[0], text='종료',command=self.quit_client)
        self.recv_label = Label(fr[1], text=' 채팅창')
        self.member_list_label= Label(fr[1], text='  port             name         ')
        self.send_label = Label(fr[3], text=' 송신메세지')
        
        self.send_btn = Button(fr[3], text='전송',command=self.send_chat)
        self.chat_transcript_area = ScrolledText(fr[2], height=20, width=60)
        self.member_list_area = ScrolledText(fr[2], height=20, width=15)
        self.enter_text_widget = ScrolledText(fr[4], height=5, width=80)
        self.name_widget = Entry(fr[0], width=15)
    
        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.recv_label.pack(side=LEFT)
        self.member_list_label.pack(side=RIGHT)
        #채팅 멤버 위치
        self.member_list_area.pack(side=RIGHT, padx=2, pady=2)

        self.quit_btn.pack(side=RIGHT, padx=20)
        self.send_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, padx=2,pady=2)
        self.send_label.pack(side=LEFT)
        self.enter_text_widget.pack(side=LEFT, padx=2, pady=2)

    def quit_client(self):
        self.close_flag = True
        self.send_chat()
        self.client_socket.close()
        self.root.destroy()

    def send_chat(self):
        # message 전송하는 callback 함수#
        if not self.close_flag:
            senders_name = self.name_widget.get().strip() + " : "
            data = self.enter_text_widget.get(1.0,'end').strip()
            self.enter_text_widget.delete("1.0","end")
            message = (senders_name + data).encode('utf-8')

        else:
            s = "close socket"
            message = s.encode('utf-8')
            print('quit message',message.decode("utf-8"))

        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def listen_thread(self):
        #thread 생성 및 시작#
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def is_json(self,myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True
    
    def receive_message(self, so):
        print("receive message func")
        #server로부터 message 수신 및 문서창 표시#
        while True:
            time.sleep(0.1)
            data = so.recv(256)
            if not data: 
                break

            if not self.is_json(data):
                print("not printed")
                continue

            #message 
            message = json.loads(data)
            self.chat_transcript_area.insert('end', message['message']+'\n')
            self.chat_transcript_area.yview(END)
            self.member_list_area.delete("1.0","end")

            #member
            for k, v in message.items():
                if k =='message':
                    continue
                self.member_list_area.insert('end', k +'  ' + v+'\n')
                self.member_list_area.yview(END)

if __name__ == "__main__":
    ip = input("server IP addr:")
    if ip == '':
        ip = '127.0.0.1'
    port = 2500
    ChatClient(ip, port)
    mainloop()
