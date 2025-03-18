import numpy as np
from Physics.QuantumComputation.Code.QuantumCode.MajoranaCode.MajoranaCode import MajoranaCode
from Physics.QuantumComputation.Code.QuantumCode.PauliCode.PauliCode import PauliCode


##  USER：将一个Pauli stabilizer code映射为Majorana stabilizer code
"""
input.pauli_code：PauliCode对象，映射原像
output：MajoranaCode对象，映射结果
"""
def pauli2majorana(pauli_code):
    ##  类型处理
    assert isinstance(pauli_code, PauliCode)
    number_qubit=pauli_code.number_qubit
    number_fermion=number_qubit*2
    number_qubit_checker=pauli_code.generator_vector.shape[0]
    number_fermion_checker=number_qubit_checker+number_qubit

    ##  添加稳定子的映射结果
    result=MajoranaCode()
    for i in range(number_qubit_checker):
        stabilizer = [0] * (number_qubit * 4)
        for j in range(number_qubit):
            X_flag_temp=pauli_code.generator_vector[i][j*2]
            Z_flag_temp=pauli_code.generator_vector[i][j*2+1]
            if X_flag_temp==1 and Z_flag_temp==0:
                stabilizer[j * 4] = 1
                stabilizer[j * 4 + 3] = 1
            elif X_flag_temp==0 and Z_flag_temp==1:
                stabilizer[j * 4+2] = 1
                stabilizer[j * 4 +3] = 1
            elif X_flag_temp==Z_flag_temp==1:
                stabilizer[j * 4+1] = 1
                stabilizer[j * 4 +3] = 1
            else:
                pass
        result.push(stabilizer,1j)

    ##  添加额外的稳定子
    for i in range(number_qubit):
        stabilizer = np.zeros(number_qubit * 4,dtype=int)
        stabilizer[i * 4] = 1
        stabilizer[i * 4+1]=1
        stabilizer[i * 4+2] = 1
        stabilizer[i * 4+3] = 1
        result.push(stabilizer,1)

    ##  返回结果
    return result