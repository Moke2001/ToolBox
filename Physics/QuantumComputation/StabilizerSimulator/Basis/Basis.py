import galois
import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.Group.Group import Group


class Basis:
    #%%  USER：构造函数
    def __init__(self,stabilizer_vector):
        self.stabilizer_vector=np.array(stabilizer_vector,dtype=Group)
        self.N=self.stabilizer_vector[0].N
        assert self.check()


    #%%  KEY：校验所有的群元对易且独立
    def check(self):
        ##  验证稳定子之间对易
        for i in range(self.stabilizer_vector.shape[0]):
            for j in range(i+1,self.stabilizer_vector.shape[0]):
                s_0=self.stabilizer_vector[i]
                s_1=self.stabilizer_vector[j]
                if not s_0.commuter(s_1):
                    return False

        ##  计算校验矩阵
        check_matrix = np.zeros((self.N,self.stabilizer_vector.shape[0]), dtype=int)
        for i in range(self.N):
            for j in range(self.stabilizer_vector.shape[0]):
                stabilizer_temp=self.stabilizer_vector[i]
                check_matrix[i,j]=stabilizer_temp[j]

        ##  计算校验矩阵的01域上的形式
        GF = galois.GF(2 ** 1)
        check_matrix = GF(check_matrix)

        ##  根据矩阵01秩计算是否独立
        if np.linalg.matrix_rank(check_matrix) == self.N:
            return True
        else:
            return False


    #%%  USER：获得下标对应的群元
    def __getitem__(self, item):
        return self.stabilizer_vector[item]
