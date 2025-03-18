import galois
import numpy as np


class Codeword:
    def __init__(self,N,codeword):
        self.N=N
        GF = galois.GF(2 ** 1)
        self.codeword=GF(np.array(codeword,dtype=int))

    def __add__(self,other):
        ##  标准化
        assert isinstance(other,Codeword),'other is not a Codeword'
        assert self.N==other.N,'N is not equal to N'

        ##  模二加法
        return Codeword(self.N,self.codeword+other.codeword)

    def __sub__(self,other):
        ##  标准化
        assert isinstance(other, Codeword), 'other is not a Codeword'
        assert self.N == other.N, 'N is not equal to N'

        ##  模二减法
        return Codeword(self.N, self.codeword - other.codeword)

    def inner(self,other):
        assert isinstance(other,Codeword), 'other is not a Codeword'
        assert self.N == other.N, 'N is not equal to N'
        result=0
        for i in range(self.N):
            result += self.codeword[i]*other.codeword[i]
        return np.mod(result,2)

    def __getitem__(self, item):
        return self.codeword[item]