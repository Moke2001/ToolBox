from Physics.QuantumComputation.ErrorCorrectionCode.PauliStabilizerCode.PauliOperator import PauliOperator
from Physics.QuantumComputation.ErrorCorrectionCode.PauliStabilizerCode.PauliStabilizerCode import PauliStabilizerCode


def majorana2css(majorana_code):
    css_code = PauliStabilizerCode(majorana_code.N * 2)
    for i in range(len(majorana_code.generator_vector)):
        stabilizer_0 = ['I'] * css_code.N
        stabilizer_1 = ['I'] * css_code.N
        for j in range(len(majorana_code.generator_vector[i])):
            if majorana_code.generator_vector[i][j] == 1:
                stabilizer_0[j] = 'X'
                stabilizer_1[j] = 'Z'
        css_code.push(PauliOperator(1,stabilizer_0))
        css_code.push(PauliOperator(1,stabilizer_1))
    return css_code