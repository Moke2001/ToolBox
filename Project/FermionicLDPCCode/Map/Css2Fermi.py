import numpy as np
from Physics.QuantumComputation.ErrorCorrectionCode.FermiStabilizerCode.MajoranaOperator import MajoranaOperator
from Physics.QuantumComputation.ErrorCorrectionCode.FermiStabilizerCode.FermiStabilizerCode import FermiStabilizerCode


def css2fermi(css_code):
    fermionic_code = FermiStabilizerCode(css_code.N)
    for i in range(len(css_code.generator_vector)):
        stabilizer = [0] * fermionic_code.N*2
        for j in range(len(css_code.generator_vector[i])):
            if css_code.generator_vector[i][j] == 'X':
                stabilizer[j*2] = 1
            elif css_code.generator_vector[i][j] == 'Z':
                stabilizer[j*2+1] = 1
            elif css_code.generator_vector[i][j] == 'Y':
                stabilizer[j*2] = 1
                stabilizer[j*2+1] = 1
        num=0
        for j in range(len(stabilizer)):
            num += stabilizer[j]
        factor=num*(num-1)/2
        if np.mod(factor,2)==0:
            eta=1j
        else:
            eta=1
        fermionic_code.push(MajoranaOperator(eta, stabilizer))

    return fermionic_code