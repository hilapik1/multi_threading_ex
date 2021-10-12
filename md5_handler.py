import hashlib

# encoding 01 using md5 hash
# function
class MD5:
    #initialize the string
    def __init__(self, word_len):
        self.result = None
        self.length=None
        self.word_len = word_len

    #encrypt a message between 0-9 letters

    def encrypt_comparer(self, word):
        self.result = self.encrypt(word)
        self.length = len(word)

    @staticmethod
    def encrypt(word): # self.result = word_encrypted
        result = hashlib.md5(word.encode())
        # printing the encrypted message byte value.
        #print("The byte encrypted message of hash is : ", end="")
        return result.hexdigest()

    def decrypt(self): # self.word_encrypted is used, output is word
        for i in range(10**self.length):
            self.word=str(i).zfill(self.word_len)
            # print(self.word)
            guess = self.encrypt(self.word)
            if guess==self.result:
            #if self.encrypt(self.word) == self.result:
                return self.word
        return ""
def main():
    word_len = 7
    md=MD5(word_len)
    bla = str(77)
    print(md.encrypt(bla))
    md.encrypt_comparer(bla.zfill(word_len))
    s = md.decrypt()
    if s != "":
        print(s)


print(__name__)
if __name__ == "__main__":
    main()