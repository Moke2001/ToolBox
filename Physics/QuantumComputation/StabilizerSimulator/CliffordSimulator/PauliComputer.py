import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.Basis.Basis import Basis
from Physics.QuantumComputation.StabilizerSimulator.Group.PauliGroup import PauliGroup


class PauliComputer:
    def __init__(self,N,p):
        self.N=N
        self.p=p
        self.psi=None

    def set_p(self):
        self.p=self.p


    def initialize(self,params):
        if params==0:
            stabilizer_vector_new=np.empty(self.N,dtype=PauliGroup)
            for i in range(self.N):
                pauli_vector_temp=np.zeros(self.N*2,dtype=int)
                pauli_vector_temp[i*2+1]=1
                stabilizer_vector_new[i]=pauli_vector_temp
            self.psi=Basis(stabilizer_vector_new)


    def X(self,index):
        assert isinstance(self.psi,Basis)
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_z=self.psi.stabilizer_vector[index][index*2+1]
            if s_z==1:
               self.psi.stabilizer_vector[index].coff=self.psi.stabilizer_vector[index].coff*(-1)


    def Y(self,index):
        assert isinstance(self.psi, Basis)
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_x = self.psi.stabilizer_vector[index][index * 2]
            s_z = self.psi.stabilizer_vector[index][index * 2 + 1]
            if not (s_z == 1 and s_x == 0):
                self.psi.stabilizer_vector[index].coff = self.psi.stabilizer_vector[index].coff * (-1)


    def Z(self,index):
        assert isinstance(self.psi, Basis)
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_x = self.psi.stabilizer_vector[i][index * 2]
            if s_x == 1:
                self.psi.stabilizer_vector[i].coff = self.psi.stabilizer_vector[index].coff * (-1)


    def H(self,index):
        assert isinstance(self.psi, Basis)
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_x = self.psi.stabilizer_vector[i][index * 2]
            s_z = self.psi.stabilizer_vector[i][index * 2 + 1]
            if s_x==1 and s_z==0:
                self.psi.stabilizer_vector[i][index*2+1]=1
                self.psi.stabilizer_vector[i][index * 2] = 0
            elif s_x==0 and s_z==1:
                self.psi.stabilizer_vector[i][index*2+1]=0
                self.psi.stabilizer_vector[i][index * 2] = 1
            elif s_x==1 and s_z==1:
                self.psi.stabilizer_vector[i].coff = self.psi.stabilizer_vector[index].coff * (-1)


    def CNOT(self,index_control,index_target):
        assert isinstance(self.psi, Basis)
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_x_control = self.psi.stabilizer_vector[i][index_control*2]
            s_z_control = self.psi.stabilizer_vector[i][index_control*2 + 1]
            s_x_target = self.psi.stabilizer_vector[i][index_target*2]
            s_z_target = self.psi.stabilizer_vector[i][index_target*2 + 1]
            temp=[0,0,0,0]
            if s_x_control==1:
                temp[0]=1
                temp[2]=1
            if s_z_control==1:
                temp[1]=1
            if s_x_target==1:
                temp[2]=np.mod(1+temp[2],2)
            if s_z_target==1:
                temp[1]=np.mod(1+temp[1],2)
                temp[3]=1
            self.psi.stabilizer_vector[i][index_control*2]=temp[0]
            self.psi.stabilizer_vector[i][index_control*2 + 1]=temp[1]
            self.psi.stabilizer_vector[i][index_target*2]=temp[2]
            self.psi.stabilizer_vector[i][index_target*2 + 1]=temp[3]


    def S(self,index):
        assert isinstance(self.psi, Basis)
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_x = self.psi.stabilizer_vector[i][index * 2]
            s_z = self.psi.stabilizer_vector[i][index * 2 + 1]
            if s_x==1:
                self.psi.stabilizer_vector[i].coff=self.psi.stabilizer_vector[index].coff*1j
                self.psi.stabilizer_vector[i][index * 2+1] = np.mod(s_z+1,2)


    def measure(self,index):
        assert isinstance(self.psi, Basis)
        flag=-1
        for i in range(self.psi.stabilizer_vector.shape[0]):
            s_x = self.psi.stabilizer_vector[i][index * 2]
            if s_x==1 and flag==-1:
                flag=i
            elif s_x==1 and flag!=-1:
                self.psi.stabilizer_vector[i]=self.psi.stabilizer_vector[i]*self.psi.stabilizer_vector[flag]
        if flag==-1:
            return 1
        else:
            if np.random.rand()<0.5:
                coff_new=1
                pauli_vector_new=np.zeros_like(self.psi.stabilizer_vector.pauli_vecctor,dtype=int)
                pauli_vector_new[index*2+1]=1
                stabilizer_new=PauliGroup(self.N,coff_new,pauli_vector_new)
                self.psi.stabilizer_vector[flag]=stabilizer_new
                return 1
            else:
                coff_new=-1
                pauli_vector_new=np.zeros_like(self.psi.stabilizer_vector.pauli_vecctor,dtype=int)
                pauli_vector_new[index*2+1]=1
                stabilizer_new=PauliGroup(self.N,coff_new,pauli_vector_new)
                self.psi.stabilizer_vector[flag]=stabilizer_new
                return 1


    def noise(self,*args):
        assert isinstance(self.psi, Basis)
        for i in range(len(args)):
            sample_temp=np.random.rand()
            if sample_temp<self.p:
                self.X(args[i])
            elif self.p<sample_temp<self.p*2:
                self.Y(args[i])
            elif self.p*2<sample_temp<self.p*3:
                self.Z(args[i])

