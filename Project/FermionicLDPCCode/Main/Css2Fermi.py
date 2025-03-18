import numpy as np
from Physics.QuantumComputation.Encoder.Code.QuantumCode.MajoranaCode import MajoranaCode
from Physics.QuantumComputation.Encoder.Code.QuantumCode.PauliCode import PauliCode


def css2majorana(css_code):
    assert isinstance(css_code,PauliCode)
    number_qubit=css_code.number_qubit
    number_qubit_checker=css_code.generator_vector.shape[0]

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

        ##  厄米系数
        num=0
        for j in range(stabilizer.shape[0]):
            num += stabilizer[j]
        factor=num*(num-1)/2
        if np.mod(factor,2)==0:
            eta=1j
        else:
            eta=1
        result.push(stabilizer,eta)

    return result
