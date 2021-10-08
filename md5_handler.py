import hashlib

# encoding 01 using md5 hash
# function
class MD5:
    #initialize the string
    def __init__(self,string):
        self.string=string
    #encrypt a message between 0-9 letters
    def encrypt(self):
        result = hashlib.md5(self.string)
        # printing the encrypted message byte value.
        print("The byte encrypted message of hash is : ", end="")
        print(result.hexdigest())

md=MD5(b'01')
md.encrypt()
