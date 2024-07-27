from random import randint
import pickle
import gmpy2
 
 
class RSA:
    def __init__(self, bits=1024, e=65537, owned=False):
        self.bits = bits
 
        while True:
            self._p = gen_prime(bits)
            self._q = gen_prime(bits)
            if self._p != self._q:  # 二者相等的极端情况
                break
        if self._p > self._q:
            self._p, self._q = self._q, self._p
        self.n = self._p * self._q
 
        assert e < self.n
        self.e = e
        self._d = pow(self.e, -1, (self._p - 1) * (self._q - 1))
 
        self.owned = owned
 
    @property
    def getP(self):
        if not self.owned:
            raise PermissionError('No permissions')
        return self._p
 
    @property
    def getQ(self):
        if not self.owned:
            raise PermissionError('No permissions')
        return self._q
 
    @property
    def getD(self):
        if not self.owned:
            raise PermissionError('No permissions')
        return self._d
 
    def encrypt(self, data):
        return pow(data, self.e, self.n)
 
    def decrypt(self, data):
        if not self.owned:
            raise PermissionError('No permissions')
        return pow(data, self._d, self.n)
 
    def __str__(self):
        res = '{n=' + str(self.n) + ', e=' + str(self.e)
        if self.owned:
            res += ', d=' + str(self._d) + ', p=' + str(self._p) + ', q=' + str(self._q)
        res += '}'
        return res
 
    def write_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
 
    @classmethod
    def read_from_file(cls, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
 
 
def gen_prime(n):
    prime = randint(3, 2 ** n)
    if prime % 2 == 0:
        prime += 1
    while not gmpy2.is_prime(prime):
        prime += 2
    return prime
