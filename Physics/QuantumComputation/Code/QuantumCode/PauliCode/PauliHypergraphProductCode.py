import numpy as np
from Algebra.BitString.BitString import BitString
from Physics.QuantumComputation.Code.ClassicalCode.LinearCode import LinearCode
from Physics.QuantumComputation.Code.QuantumCode.PauliCode.PauliCode import PauliCode


##  KEY：定位某坐标qubit的一维序号
"""
input.pos：tuple of int and int对象，qubit的二维坐标
input.number_checker_0：int对象，线性码0的奇偶校验子的数目
input.number_checker_1：int对象，线性码1的奇偶校验子的数目
input.number_bit_0：int对象，线性码0的比特数目
input.number_bit_1：int对象，线性码1的比特数目
output：int对象，qubit的一维坐标，从下往上，从左往右，先右后上
"""
def qubit_index(pos,number_checker_0,number_checker_1,number_bit_0,number_bit_1):
    pos_X=pos[0]
    pos_Y=pos[1]
    if pos_X<number_checker_0 and pos_Y<number_checker_1:
        index=pos_Y*number_bit_0+pos_X
    elif pos_X>=number_checker_0 and pos_Y>=number_bit_1:
        index=number_checker_0*number_checker_1+(pos_X-number_bit_0)+(pos_Y-number_bit_1)*number_bit_0
    else:
        raise IndexError
    return index


##  USER：用两个经典码构造Pauli hypergraph product code
"""
input.C_0：LinearCode对象，线性码0
input.C_1：LinearCode对象，线性码1
output：PauliCode对象，合成的Pauli stabilizer code
"""
def pauli_hypergraph_product_code(C_0,C_1):

    ##  规范步骤
    assert isinstance(C_0,LinearCode)
    assert isinstance(C_1,LinearCode)

    ##  获取线性码的bit数目和校验子数目
    checker_vector_0=C_0.get_checkers().copy()
    checker_vector_1=C_1.get_checkers().copy()

    ##  增加非独立的校验子
    checker_0=None
    for i in range(checker_vector_0.shape[0]):
        if i==0:
            checker_0=checker_vector_0[i]
        else:
            checker_0=checker_0+checker_vector_0[i]
    checker_vector_0=np.append(checker_vector_0, np.array([checker_0], dtype=BitString))
    number_checker_0=checker_vector_0.shape[0]
    number_bit_0=len(checker_0)

    ##  增加非独立的校验子
    checker_1=None
    for i in range(checker_vector_1.shape[0]):
        if i==0:
            checker_1=checker_vector_1[i]
        else:
            checker_1=checker_1+checker_vector_1[i]
    checker_vector_1=np.append(checker_vector_1, np.array([checker_1], dtype=BitString))
    number_checker_1=checker_vector_1.shape[0]
    number_bit_1=len(checker_1)


    ##  构成直积码
    number_qubit=number_checker_0*number_checker_0+number_bit_0*number_bit_0
    pauli_code = PauliCode()
    for pos_X in range(number_checker_0+number_bit_0):
        for pos_Y in range(number_checker_0+number_bit_0):

            ##  添加右下角区块的校验子
            if pos_X >= number_checker_0 and pos_Y<number_checker_1:
                data_vector = np.zeros(number_qubit * 2, dtype=int)

                ##  包括上面的qubits
                for i in range(len(checker_vector_1[pos_Y])):
                    if checker_vector_1[pos_Y][i]==1:
                        data_vector[qubit_index((pos_X,number_checker_1+i),
                                                number_checker_0,
                                                number_checker_1,
                                                number_bit_0,
                                                number_bit_1)*2]=1

                ##  包括左边的qubits
                for i in range(number_checker_0):
                    if checker_vector_0[i][pos_X-number_checker_0] == 1:
                        data_vector[qubit_index((i, pos_Y),
                                                number_checker_0,
                                                number_checker_1,
                                                number_bit_0,
                                                number_bit_1) * 2] = 1

                ##  添加稳定子生成元
                pauli_code.push(data_vector,1)

            ##  添加左上角区块的校验子
            elif pos_X < number_checker_0 and pos_Y >= number_checker_1:
                data_vector = np.zeros(number_qubit * 2, dtype=int)

                ##  包括右侧的qubits
                for i in range(len(checker_vector_0[pos_X])):
                    if checker_vector_0[pos_X][i]==1:
                        data_vector[qubit_index((number_checker_0+i,pos_Y),
                                                number_checker_0,
                                                number_checker_1,
                                                number_bit_0,
                                                number_bit_1)*2+1]=1

                ##  包括下面的qubits
                for i in range(number_checker_1):
                    if checker_vector_1[i][pos_Y-number_checker_1] == 1:
                        data_vector[qubit_index((pos_X, i),
                                                number_checker_0,
                                                number_checker_1,
                                                number_bit_0,
                                                number_bit_1) * 2+1] = 1

                ##  添加稳定子生成元
                pauli_code.push(data_vector,1)

    ##  返回结果
    return pauli_code