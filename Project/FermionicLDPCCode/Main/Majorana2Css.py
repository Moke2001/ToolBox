import numpy as np
from Physics.QuantumComputation.Encoder.Code.QuantumCode.MajoranaCode import MajoranaCode
from Physics.QuantumComputation.Encoder.Code.QuantumCode.PauliCode import PauliCode


def majorana2css(majorana_code):
    assert isinstance(majorana_code, MajoranaCode)
    ##  提取信息
    number_fermion=majorana_code.number_fermion
    number_qubit=number_fermion*2
    number_fermion_checker=majorana_code.generator_vector.shape[0]

    ##  生成Pauli稳定子生成元
    result=PauliCode()
    for i in range(number_fermion_checker):
        qubit_list_0 = np.zeros(number_qubit*2,dtype=int)
        qubit_list_1 = np.zeros(number_qubit*2,dtype=int)
        for j in range(number_fermion*2):
            if majorana_code.generator_vector[i][j] == 1:
                qubit_list_0[j*2] = 1
                qubit_list_1[j*2+1] = 1
        result.push(qubit_list_0,1)
        result.push(qubit_list_1,1)

    ##  返回结果
    return result