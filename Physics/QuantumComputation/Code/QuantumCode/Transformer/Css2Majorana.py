import numpy as np
from Physics.QuantumComputation.Code.QuantumCode.MajoranaCode.MajoranaCode import MajoranaCode
from Physics.QuantumComputation.Code.QuantumCode.PauliCode.PauliCode import PauliCode


##  USER：将一个weakly self-dual CSS code映射为一个Majorana stabilizer code
"""
input.css_code：PauliCode对象，要求是一个weakly self-dual CSS code
output：MajoranaCode对象，映射结果
"""
def css2majorana(css_code):
    ##  类型处理
    assert isinstance(css_code,PauliCode)
    number_qubit=css_code.number_qubit
    number_qubit_checker=css_code.generator_vector.shape[0]

    ##  将每一个Pauli稳定子映射为Majorana稳定子
    result=MajoranaCode()
    for i in range(number_qubit_checker):
        stabilizer = np.zeros(number_qubit * 2,dtype=int)
        for j in range(number_qubit):
            X_flag=css_code.generator_vector[i][j*2]
            Z_flag=css_code.generator_vector[i][j*2+1]
            assert X_flag!=Z_flag or X_flag==Z_flag==0
            if X_flag==1:
                stabilizer[j*2] = 1
            elif Z_flag==1:
                stabilizer[j*2+1] = 1

        ##  厄米系数重新生成
        num=0
        for j in range(stabilizer.shape[0]):
            num += stabilizer[j]
        factor=num*(num-1)/2
        if np.mod(factor,2)==0:
            eta=1j
        else:
            eta=1
        result.push(stabilizer,eta)

    ##  返回结果
    return result
