import numpy as np
from Algebra.BitString.BitString import BitString
from Physics.QuantumComputation.Code.ClassicalCode.EuclideanCode import EuclideanCode
from Physics.QuantumComputation.Code.ClassicalCode.LinearCode import LinearCode
from Physics.QuantumComputation.Code.QuantumCode.PauliCode.PauliCode import PauliCode


class CSSCode(PauliCode):
    def __init__(self,C_0,C_1):
        assert isinstance(C_0,LinearCode)
        assert isinstance(C_1,LinearCode)
        super().__init__()
        X_checker_vector=C_0.get_checkers()
        Z_checker_vector=C_1.get_checkers()
        for i in range(len(X_checker_vector)):
            temp=X_checker_vector[i]
            assert isinstance(temp,BitString)
            pauli_checker_temp=np.zeros(temp.number_bit*2,dtype=int)
            for j in range(temp.number_bit):
                if temp[j]==1:
                    pauli_checker_temp[j*2]=1
            self.push(pauli_checker_temp)
        for i in range(len(Z_checker_vector)):
            temp=Z_checker_vector[i]
            assert isinstance(temp,BitString)
            pauli_checker_temp=np.zeros(temp.number_bit*2,dtype=int)
            for j in range(temp.number_bit):
                if temp[j]==1:
                    pauli_checker_temp[j*2]=1
            self.push(pauli_checker_temp)


