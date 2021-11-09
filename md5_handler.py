import hashlib
import select
import socket
# encoding 01 using md5 hash
# function
class  handler:
    def __init__(self, socket):
        self.client_socket = socket
        self.start=None
        self.end=None
        self.encrypt_msg=None
        self.len=None
        self.size_of_len=None
    def send_initial_message(self):
        message="more work"
        len_message=len(message.encode())
        self.client_socket.send(str(len_message).zfill(4).encode())
        self.client_socket.send(str(message).encode())

    def send_done_message(self):
        message = "Done"
        len_message = len(message.encode())
        self.client_socket.send(str(len_message).zfill(4).encode())
        self.client_socket.send(str(message).encode())

    def recv_initial_encrypted_message(self):
        len_message = self.client_socket.recv(4)
        message=self.client_socket.recv(int(len_message.decode))
        list=message.split(',')#encrypt_msg, len, size of len
        self.encrypt_msg=list[0]
        self.len=list[1]
        self.size_of_len=list[2]

    def recv_range(self):
        len_message = self.client_socket.recv(4)
        data= self.client_socket.recv(int(len_message.decode))#'start,end'
        data=data.decode()
        list_range=data.split(',')
        self.start=list_range[0] #start
        self.end = list_range[1] #end

class MD5:
    #initialize the string
    def __init__(self, word_len,socket):
        self.result = None
        self.length=None
        self.word_len = word_len
        self.client_socket = socket

    #encrypt a message between 0-9 letters

    def create_encrypt_comparer(self, word):
        self.result = self.encrypt(word)
        self.length = len(word)



    @staticmethod
    def encrypt(word): # self.result = word_encrypted
        result = hashlib.md5(word.encode())
        # printing the encrypted message byte value.
        #print("The byte encrypted message of hash is : ", end="")
        return result.hexdigest()
    # 10**self.length
    def decrypt(self,range_obj):
        """Convert a numeric family value to an IntEnum member.
            self.word_encrypted is used, output is word
            If it's not a known member, return the numeric value itself.
            """
        # self.word_encrypted is used, output is word
        for start in range_obj:
            self.word=str(start).zfill(self.word_len)
            # print(self.word)
            guess = self.encrypt(self.word)
            if guess==self.result:
            #if self.encrypt(self.word) == self.result:
                return self.word
        return ""


def init_network():
    client_socket = socket.socket()
    client_socket.connect(("127.0.0.1", 5555))
    return client_socket


def main():
    client_socket = init_network()
    word_len = 7
    md = MD5(word_len, client_socket)
    bla = str(77)
    print(md.encrypt(bla))
    md.create_encrypt_comparer(bla.zfill(word_len))
    start = 0
    jump=0
    initial_mes=handler(client_socket)
    initial_mes.send_initial_message()#announce the server for beggining- ask for work
    while True:
        rlist, wlist, xlist = select.select([client_socket], [], [], 1)
        for sock in rlist:
            start = int(sock.recv(1024).decode())
            jump = int(sock.recv(1024).decode())#for example  start + 10000 jump=10000
            s = md.decrypt(range(start, start + jump))
            if s != "":
                initial_mes.send_done_message()#send to server that the client found
                print(s)
                ok=sock.recv(1024).decode()#server say ok- work finished
                if ok=="OK":
                    break #check how to say to all the clients to stop their work
            else:
                initial_mes.send_initial_message()#the client ask for more work


print(__name__)
if __name__ == "__main__":
    main()