import select
import socket
import time
from datetime import datetime
from datetime import date

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
MIN_NUM=0
MAX_NUM=10000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()


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
                    length_mes = current_socket.recv(1024)#.decode()
                    if length_mes=="":
                        self.clients_socket.remove(current_socket)
                        # if clients_socket == []:
                        #     server_socket.close()
                    else:
                        length_mes=length_mes.decode()
                        optional_msg = current_socket.recv(1024).decode()
                        if optional_msg == "more work":
                            msg="work "+str(MIN_NUM)+" "+str(MAX_NUM)
                            len_msg=str(len(msg))
                            current_socket.send(len_msg.encode())
                            time.sleep(0.1)
                            current_socket.send(msg.encode())
                        elif optional_msg=="Done":
                            msg = "Done"
                            len_msg = str(len(msg))
                            for socket in self.clients_socket:
                                if(current_socket==socket):
                                    continue
                                socket.send(len_msg.encode())
                                time.sleep(0.1)
                                socket.send(msg.encode())
                                self.clients_socket.remove(socket)




def main():
    user1 = server(server_socket)
    user1.server_functions()

if __name__ == "__main__":
    main()