import pickle
from Crypto.Cipher import AES
from Crypto.Hash import MD5
 
from RSA import *
import time
 
class AESCipher:
    def __init__(self, key):
        self.bs = AES.block_size
        self.mode = AES.MODE_ECB
        self.key = key
 
    def encrypt(self, data):
        cipher = AES.new(self.key, self.mode)
        ct = cipher.encrypt(data)
        return ct
 
    def decrypt(self, ct):
        try:
            cipher = AES.new(self.key, self.mode)
            data = cipher.decrypt(ct)
            return data
        except (ValueError, KeyError) as err:
            print("Incorrect decryption ", err)
            return None
 
 
def my_MD5(data):
    cipher = MD5.new(data)
    return cipher.digest()
 
 
def int_to_bytes(num, length=256):
    return num.to_bytes(length, 'little', signed=False)
 
 
def bytes_to_int(this_bytes):
    return int.from_bytes(this_bytes, 'little', signed=False)
 
 
def ring_sig_sign(rsa_user, rsa_list, key):
    aes_cipher = AESCipher(key)
    user_index = randint(0, len(rsa_list))
 
    xlist = []
    ylist = []
    for i in range(len(rsa_list)):
        x = randint(3, rsa_list[i].n - 1)
        y = rsa_list[i].encrypt(x)
        xlist.append(x)
        ylist.append(y)
 
    while True:
        v = randint(1, 2 ** 2048 - 1)
        ek_former = v
        for i in range(user_index):
            ek_former = bytes_to_int(aes_cipher.encrypt(int_to_bytes(ylist[i] ^ ek_former)))
        ek_latter = v
        for i in range(len(rsa_list) - 1, user_index - 1, -1):
            ek_latter = ylist[i] ^ bytes_to_int(aes_cipher.decrypt(int_to_bytes(ek_latter)))
        y_user = ek_former ^ bytes_to_int(aes_cipher.decrypt(int_to_bytes(ek_latter)))
 
        if y_user < rsa_user.n:
            break
 
    x_user = rsa_user.decrypt(y_user)
    xlist.insert(user_index, x_user)
    rsa_list.insert(user_index, rsa_user)
    return rsa_list, v, xlist
 
 
def ring_sig_verify(rsa_list, v, xlist, key):
    assert len(rsa_list) == len(xlist)
 
    aes_cipher = AESCipher(key)
 
    ek = v
    for i in range(len(rsa_list)):
        yi = rsa_list[i].encrypt(xlist[i])
        ek = bytes_to_int(aes_cipher.encrypt(int_to_bytes(yi ^ ek)))
    return ek == v


class Cat:
    def __init__(self):
        self.a = "1"
        self.b = "2"

 
if __name__ == '__main__':
    st = time.time()

    key = my_MD5(pickle.dumps(Cat()))
    for i in range(0,5):
        rsaAlice = RSA(owned=True)
        rsa1 = RSA()
        rsa2 = RSA()
        rsa3 = RSA()
        rsa4 = RSA()
        rsa5 = RSA()
        rsa6 = RSA()
        rsa7 = RSA()
        rsa8 = RSA()
        rsa9 = RSA()
        rsa10 = RSA()
        rsaList, v, xList = ring_sig_sign(rsaAlice, [rsa1, rsa2, rsa3, rsa4, rsa5, rsa6, rsa7, rsa8, rsa9, rsa10], key)
        # print(v)
        # for i in range(10):
        #     print(rsaList[i])
        #     print(xList[i])

        # print(ring_sig_verify(rsaList, v, xList, key))
        et = time.time()
        print(format(et-st))