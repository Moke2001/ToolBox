import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.Basis.Basis import Basis
from Physics.QuantumComputation.StabilizerSimulator.Group.MajoranaGroup import MajoranaGroup


class MajoranaComputer:
    def __init__(self,N,p):
        self.N=N
        self.p=p
        self.psi=None

    def initialize(self,params):
        if params==0:
            stabilizer_vector_new=np.empty(self.N,dtype=MajoranaGroup)
            for i in range(self.N):
                majorana_vector_temp=np.zeros(self.N*2,dtype=int)
                majorana_vector_temp[i*2] = 1
                majorana_vector_temp[i*2+1]=1
                stabilizer_vector_new[i]=MajoranaGroup(self.N,-1,majorana_vector_temp)
            self.psi=Basis(stabilizer_vector_new)
        elif params==1:
            stabilizer_vector_new=np.empty(self.N,dtype=MajoranaGroup)
            for i in range(self.N):
                majorana_vector_temp=np.zeros(self.N*2,dtype=int)
                majorana_vector_temp[i*2] = 1
                majorana_vector_temp[i*2+1]=1
                stabilizer_vector_new[i]=MajoranaGroup(self.N,1,majorana_vector_temp)
            self.psi=Basis(stabilizer_vector_new)


    def Phase(self,index):
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_0=self.psi.stabilizer_vector[index*2]
            s_1=self.psi.stabilizer_vector[index*2+1]
            if (s_0==1 and s_1==0) or (s_0==0 and s_1==1):
                self.psi.stabilizer_vector[index*2].coff=-self.psi.stabilizer_vector[index*2].coff



    def gamma(self,index):
        majorana_vector_temp=np.zeros(self.N*2,dtype=int)
        majorana_vector_temp[index] = 1
        error=MajoranaGroup(self.N,1,majorana_vector_temp)
        flag = -1
        for i in range(self.psi.stabilizer_vector.shape[0]):
            if (not error.commuter(self.psi.stabilizer_vector[i])) and flag==-1:
                flag=i
                self.psi.stabilizer_vector[i].coff=-self.psi.stabilizer_vector[i].coff
            elif (not error.commuter(self.psi.stabilizer_vector[i])) and flag!=-1:
                self.psi.stabilizer_vector[i]=self.psi.stabilizer_vector[flag]*self.psi.stabilizer_vector[i]


    def measure(self,index):
        flag=-1
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_0 = self.psi.stabilizer_vector[i][index * 2]
            s_1 = self.psi.stabilizer_vector[i][index * 2 + 1]
            if ((s_0==1 and s_1==0) or (s_0==0 and s_1==1)) and flag==-1:
                flag=i
            elif ((s_0==1 and s_1==0) or (s_0==0 and s_1==1)) and flag!=-1:
                self.psi.stabilizer_vector[i]=self.psi.stabilizer_vector[i]*self.psi.stabilizer_vector[flag]

        if flag==-1:
            return 1

        else:
            if np.random.rand()<0.5:
                coff_new=1
                majorana_vector_new=np.zeros_like(self.psi.stabilizer_vector.pauli_vecctor,dtype=int)
                majorana_vector_new[index*2]=1
                majorana_vector_new[index * 2+1] = 1
                stabilizer_new=MajoranaGroup(self.N,coff_new,majorana_vector_new)
                self.psi.stabilizer_vector[flag]=stabilizer_new
                return 1
            else:
                coff_new=-1
                majorana_vector_new=np.zeros_like(self.psi.stabilizer_vector.pauli_vecctor,dtype=int)
                majorana_vector_new[index*2]=1
                majorana_vector_new[index * 2+1] = 1
                stabilizer_new=MajoranaGroup(self.N,coff_new,majorana_vector_new)
                self.psi.stabilizer_vector[flag]=stabilizer_new
                return -1


    def noise(self,*args):
        for i in range(len(args)):
            sample_temp=np.random.rand()
            if sample_temp<self.p:
                self.gamma(args[i]*2)
            elif self.p<sample_temp<self.p*2:
                self.gamma(args[i]*2+1)