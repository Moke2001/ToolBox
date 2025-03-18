import copy
import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.Group.Group import Group


class PauliGroup(Group):
    def __init__(self,N,coff,pauli_vector):
        super().__init__(N)
        assert self.N*2==len(pauli_vector)
        self.pauli_vector=np.array(pauli_vector,dtype=int)
        self.coff=coff

    def __mul__(self,other):
        ##  如果对方是PauliGroup对象
        if isinstance(other, PauliGroup):
            assert self.N==other.N
            ##  计算相乘结果
            pauli_vector_new = np.zeros_like(self.pauli_vector,dtype=int)  # 新算符
            coff_new = self.coff * other.coff  # 新算符的系数
            for i in range(int(self.pauli_vector.shape[0]/2)):
                if self.pauli_vector[i*2+1]==other.pauli_vector[i*2]:
                    coff_new=coff_new*(-1)
            pauli_vector_new=np.mod(self.pauli_vector+other.pauli_vector,2)

            ##  返回结果
            return PauliGroup(self.N,coff_new,pauli_vector_new)

        ##  如果对方是数，则与系数直接计算
        elif isinstance(other, complex) or isinstance(other, int):
            new_pauli_vector = self.pauli_vector.copy()
            return PauliGroup(self.N,self.coff * other, new_pauli_vector)

        else:
            raise NotImplementedError


    def __rmul__(self,other):
        if isinstance(other, PauliGroup):
            return other.__mul__(other)
        elif isinstance(other, complex) or isinstance(other, int):
            return self.__mul__(other)


    def __eq__(self, other):
        assert self.N==other.N
        if np.all(self.pauli_vector==other.majorana_vector):
            return True
        else:
            return False


    # %%  USER：复制函数
    """
    output：PauliOperator对象，复制结果
    """
    def copy(self):
        return copy.deepcopy(self)


    # %%  USER：算符共轭
    """
    output：PauliOperator对象，共轭结果
    """
    def dag(self):
        if self.coff == 1 or self.coff == -1:
            return self.copy()
        else:
            result = self.copy()
            result.coff = -self.coff
            return result


    # %%  USER：对易式
    def commuter(self, other):
        temp_0 = self * other
        temp_1 = other * self
        return temp_0.coff == temp_1.coff


    def __getitem__(self, item):
        if isinstance(item,int):
            return self.pauli_vector[item]
        elif isinstance(item,tuple):
            index_0=item[0]
            index_1=item[1]
            return self.pauli_vector[index_0*2+index_1]

