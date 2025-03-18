import numpy as np
from Physics.QuantumComputation.Encoder.BitString.BitString import BitString
from Physics.QuantumComputation.Encoder.Code.ClassicalCode.LinearCode import LinearCode
from Physics.QuantumComputation.Encoder.Code.QuantumCode.PauliCode import PauliCode


def qubit_index(pos,N_C,N_B):
    pos_X=pos[0]
    pos_Y=pos[1]
    assert (pos_X<N_C and pos_Y<N_C) or (pos_X>=N_C and pos_Y>=N_C)
    index=0
    if pos_X<N_C and pos_Y<N_C:
        index=pos_Y*N_C+pos_X
    elif pos_X>=N_C and pos_Y>=N_C:
        index=N_C*N_C+(pos_X-N_C)+(pos_Y-N_C)*N_B
    return index


def pauli_hypergraph_product_code(C):
    assert isinstance(C,LinearCode)

    ##  获取线性码的bit数目和校验子数目
    checker_vector=C.get_checkers().copy()

    ##  增加非独立的校验子
    checker_0=None
    for i in range(checker_vector.shape[0]):
        if i==0:
            checker_0=checker_vector[i]
        else:
            checker_0=checker_0+checker_vector[i]

    checker_vector=np.append(checker_vector, np.array([checker_0], dtype=BitString))
    number_checker=checker_vector.shape[0]
    number_bit=len(checker_vector[0])

    ##  构成直积码
    number_qubit=number_checker*number_checker+number_bit*number_bit
    pauli_code = PauliCode()
    for pos_X in range(number_checker+number_bit):
        for pos_Y in range(number_checker+number_bit):
            if pos_X >= number_checker > pos_Y:
                pauli_vector = np.zeros(number_qubit * 2, dtype=int)
                for i in range(len(checker_vector[pos_Y])):
                    if checker_vector[pos_Y].get_bit(i)==1:
                        pauli_vector[qubit_index((pos_X,number_checker+i),number_checker,number_bit)*2]=1
                for i in range(number_checker):
                    if checker_vector[i].get_bit(pos_X-number_checker) == 1:
                        pauli_vector[qubit_index((i, pos_Y), number_checker, number_bit) * 2] = 1
                pauli_code.push(pauli_vector,1)
                pos_X_0=pos_Y
                pos_Y_0=pos_X
                pauli_vector = np.zeros(number_qubit * 2, dtype=int)
                for i in range(len(checker_vector[pos_X_0])):
                    if checker_vector[pos_X_0].get_bit(i)==1:
                        pauli_vector[qubit_index((number_checker+i,pos_Y_0),number_checker,number_bit)*2+1]=1
                for i in range(number_checker):
                    if checker_vector[i].get_bit(pos_Y_0-number_checker) == 1:
                        pauli_vector[qubit_index((pos_X_0,i), number_checker, number_bit) * 2 + 1] = 1
                pauli_code.push(pauli_vector,1)

    ##  返回结果
    return pauli_code