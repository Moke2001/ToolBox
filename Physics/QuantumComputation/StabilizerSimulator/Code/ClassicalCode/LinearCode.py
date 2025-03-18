import galois
import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.Code.ClassicalCode.ClassicalCode import ClassicalCode

from Physics.QuantumComputation.StabilizerSimulator.Code.ClassicalCode.Codeword import Codeword


class LinearCode:
    def __init__(self,N,codewords):
        self.N=N
        self.codewords=np.array(codewords,dtype=Codeword)

    def get_check_matrix(self):


    def get_generate_matrix(self):
        GF = galois.GF(2 ** 1)
        generate_matrix=GF(np.zeros((self.codewords.shape[0],self.N)))
        for i in range(self.codewords.shape[0]):
            for j in range(self.N):
                generate_matrix[i,j]=self.codewords[i][j]
        return generate_matrix


    def get_dual_code(self):
        

    def get_dual_code(self):
        check_matrix = np.zeros((len(self.checkers), self.N), dtype=int)
        for i in range(len(self.checkers)):
            for j in range(self.N):
                check_matrix[i, j] = self.checkers[i][j]
        GF = galois.GF(2 ** 1)
        check_matrix = GF(check_matrix)
        nullspace = check_matrix.null_space()
        new_code=LinearCode(len(self.checkers))
        for i in range(nullspace.shape[0]):
            new_code.push(nullspace[i])
        return new_code

    def check(self ,codeword):
        GF = galois.GF(2**1)
        codeword_GF = GF(codeword)
        for i in range(len(self.checkers)):
            checker_GF=GF(codeword_GF)
            if checker_GF.dot(codeword_GF)==1:
                return False
        return True

if __name__=='__main__':
    code=LinearCode(3)
    code.push(np.array([1,1,0],dtype=int))
    code.push(np.array([0,1,1],dtype=int))
    code.get_dual_code()
    pass
