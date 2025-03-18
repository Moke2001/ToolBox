import numpy as np

from Algebra.BitString.BitString import BitString
from Physics.QuantumComputation.Code.ClassicalCode.LinearCode import LinearCode


class EuclideanCode(LinearCode):
    def __init__(self):
        super().__init__()
        H_0=np.zeros((7,7),dtype=int)
        H_1=np.zeros((7,7),dtype=int)
        H_2=np.zeros((7,7),dtype=int)
        for i in range(7):
            H_0[i,np.mod(i+0,7)]=1
            H_0[i,np.mod(i+4,7)]=1
            H_1[i,np.mod(i+0,7)]=1
            H_1[i,np.mod(i+5,7)]=1
            H_2[i,np.mod(i+0,7)]=1
            H_2[i,np.mod(i+6,7)]=1
        H_0_T=H_0.T
        H_1_T=H_1.T
        H_2_T=H_2.T
        checker_list=[]
        for i in range(7):
            bitstring_temp=BitString()
            temp=np.append(H_0_T[i,:],H_1_T[i,:])
            temp=np.append(temp,H_2_T[i,:])
            temp=np.append(temp,H_0[i,:])
            temp=np.append(temp,H_1[i,:])
            temp=np.append(temp,H_2[i,:])
            bitstring_temp.define(temp)
            checker_list.append(bitstring_temp)
        self.codewords_define(checker_list)