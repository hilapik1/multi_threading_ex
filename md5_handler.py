import hashlib

# encoding 01 using md5 hash
# function
class MD5:
    #initialize the string
    def _init_(self):
        self.result = None
        self.length=None
    #encrypt a message between 0-9 letters

    def encrypt_comparer(self, word):
        self.result = self.encrypt(word)
        self.length = len(word)

    @staticmethod
    def encrypt(word): # self.result = word_encrypted
        result = hashlib.md5(word)
        # printing the encrypted message byte value.
        #print("The byte encrypted message of hash is : ", end="")
        #print(result.hexdigest())
        return result

    def decrypt(self): # self.word_encrypted is used, output is word
        for i in range(10**self.length):
            self.word=i.to_bytes(2, 'big')
            print(self.word)
            if self.encrypt(self.word)==self.result:
                print(i)
                return
md=MD5()
md.encrypt_comparer(b'01')
md.decrypt()