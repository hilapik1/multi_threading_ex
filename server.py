import select
import socket
import time
from datetime import datetime
from datetime import date

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Hi")


class server:
    def  __init__(self,server_socket):
        self.server_soc=server_socket
        self.TosendTo = []
        self.TosendTo1 = []
        self.list_of_Names = []
        self.name_count = 0
        self.clients_socket = []
        self.messages_to_send = []  # ( dstClient ,  data )
        self.AddrDict = {}
        self.type_message = []

    def Calculate_Time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        time = current_time.split(':')
        time_update = time[0] + ':' + time[1]
        return time_update
        # print(time_update)

    def Calculate_Date(self):
        today = date.today()
        # Textual month, day and year
        d2 = today.strftime("%B %d, %Y")
        # print("d2 =", d2)
        return d2;

    def server_functions(self):
        while True:

            rlist, wlist, xlist = select.select([server_socket] + self.clients_socket, self.clients_socket, [])

            for current_socket in rlist:
                if current_socket is server_socket:
                    (connection, client_address) = current_socket.accept()
                    print("New client joined! {} con {} ".format(client_address, connection))
                    self.clients_socket.append(connection)
                else:
                    length_mes = current_socket.recv(4)#.decode()
                    if length_mes==b'':
                        self.clients_socket.remove(current_socket)
                        # if clients_socket == []:
                        #     server_socket.close()
                    else:
                        length_mes=length_mes.decode()
                        optional_msg = current_socket.recv(int(length_mes)).decode()
                        type_message = optional_msg.split('$')
                        if type_message[0] == "name":
                            print(type_message[1])
                            self.list_of_Names.append(type_message[1])
                            d = {current_socket: self.list_of_Names[self.name_count % len(self.list_of_Names)]}
                            print(self.list_of_Names[self.name_count % len(self.list_of_Names)])
                            self.name_count += 1
                            self.AddrDict.update(d)
                            print(self.AddrDict)
                            cur_date = self.Calculate_Date()
                            #current_socket.send(cur_date.encode())
                        elif type_message[0] == "message":
                            if type_message[1] == "":
                                print(" Connection closed ")
                                self.clients_socket.remove(current_socket)
                                self.AddrDict.pop(current_socket)
                                current_socket.close()
                            else:
                                print(" {} >> {} ".format(self.AddrDict.get(current_socket), type_message[1]))
                                TosendTo = self.clients_socket.copy()
                                TosendTo.remove(current_socket)  # len = amount connected - 1
                                print(type(type_message[1]))
                                print(type_message[1])
                                print(type(self.AddrDict.get(current_socket)))
                                print(self.AddrDict.get(current_socket))
                                time_cur=self.Calculate_Time()
                                self.messages_to_send.append((TosendTo,time_cur +" "+ str(self.AddrDict.get(current_socket)) + ": " + type_message[1]))
                        elif type_message[0] == "quit":
                             self.clients_socket.remove(current_socket)
                             # if clients_socket == []:
                             #    server_socket.close()
                        elif type_message[0] == "image":
                            codelen= current_socket.recv(4)
                            code_emoji=current_socket.recv(int(codelen))
                            TosendTo1 = self.clients_socket.copy()
                            TosendTo1.remove(current_socket)  # len = amount connected - 1
                            for s in self.clients_socket:
                                if s in wlist and s != current_socket:
                                    # send image message prefix
                                    s.send(str("image$"+code_emoji.decode()+"$"+str(self.AddrDict.get(current_socket))).encode())
                                    t="image$"+code_emoji.decode()
                                    f=str("image$"+code_emoji.decode()+"$"+str(self.AddrDict.get(current_socket))).encode()
                                    print(f)
                                    #print(t)
                                    #time.slep(0.6)
                                    # send image code length
                                    #s.send(codelen)
                                    # send image code
                                    #s.send(code_emoji)

            for message in self.messages_to_send:
                (SocketsToSend, data) = message
                for current_socket in SocketsToSend:
                    if current_socket in wlist:
                        current_socket.send("message$".encode())
                        #time.sleep(0.6)
                        current_socket.send(data.encode())
                        SocketsToSend.remove(current_socket)
                if not SocketsToSend:  # SocketToSend is empty
                    self.messages_to_send.remove(message)


def main():
    user1 = server(server_socket)
    user1.server_functions()

if __name__ == "__main__":
    main()