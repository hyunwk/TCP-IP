from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *
import time
import json
class ChatClient:
    client_socket = None

    def __init__(self, ip, port):
        self.initialize_socket(ip,port)
        self.initialize_gui()
        self.listen_thread()
        self.listen_member_thread()

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
        self.recv_label = Label(fr[1], text=' 채팅창')
        self.member_list_label= Label(fr[1], text='참여자                      ')
        self.send_label = Label(fr[3], text=' 송신메세지')
        # 채팅 멤버 라벨
        #self.member_list_label = Label(fr[5], text='채팅멤버')
        # 채팅 멤버 area
        #self.member_list_area = ScrolledText(fr[6], height=20, width=20)
        
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

        self.send_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, padx=2,pady=2)
        self.send_label.pack(side=LEFT)
        self.enter_text_widget.pack(side=LEFT, padx=2, pady=2)

    def send_chat(self):
        # message 전송하는 callback 함수#

        senders_name = self.name_widget.get().strip() + " : "
        data = self.enter_text_widget.get(1.0,'end').strip()
        message = (senders_name + data +'\n').encode('utf-8')
        self.chat_transcript_area.insert('end',message.decode("utf-8"))
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'


    def listen_thread(self):
        #thread 생성 및 시작#
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def listen_member_thread(self):
        #thread 생성 및 시작#
        m = Thread(target=self.receive_member, args=(self.client_socket,))
        m.start()

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def receive_message(self, so):
        #server로부터 message 수신 및 문서창 표시#
        while True:
            data = so.recv(256)
            if not data:
                break
            message = data.decode('utf-8').strip()
            print ('message',message.rstrip()[message.find(":")+2:])
            if message.rstrip()[message.find(":")+2:] == "/q":
                print("close sock")
                so.close()
            self.chat_transcript_area.insert('end', message)
            self.chat_transcript_area.yview(END)

    def receive_member(self, so):
        #server로부터 message 수신 및 문서창 표시#
        while True:
            data = so.recv(256)
            data_loaded = json.loads(data)
            if not data_loaded:
                break
            for data in data_loaded:

            message = data.decode('utf-8').strip()
            print ('message',message.rstrip()[message.find(":")+2:])
            if message.rstrip()[message.find(":")+2:] == "/q":
                print("close sock")
                so.close()
            self.chat_transcript_area.insert('end', message)
            self.chat_transcript_area.yview(END)

if __name__ == "__main__":
    ip = input("server IP addr:")
    if ip == '':
        ip = '127.0.0.1'
    port = 2500
    ChatClient(ip, port)
    mainloop()
