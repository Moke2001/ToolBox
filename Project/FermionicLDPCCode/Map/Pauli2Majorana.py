from QuantumComputation.ErrorCorrectionCode.FermiStabilizerCode.MajoranaOperator import MajoranaOperator
from QuantumComputation.ErrorCorrectionCode.FermiStabilizerCode.FermiStabilizerCode import FermiStabilizerCode


def pauli2majorana(pauli_code):
    majorana_code = FermiStabilizerCode(pauli_code.N * 2)
    ##  添加稳定子的映射结果
    for i in range(len(pauli_code.stabilizers)):
        stabilizer = [0] * (pauli_code.N * 4)
        for j in range(len(pauli_code.stabilizers[i])):
            if pauli_code.stabilizers[i][j] == 'X':
                stabilizer[j * 4] = 1
                stabilizer[j * 4 + 3] = 1
            elif pauli_code.stabilizers[i][j] == 'Z':
                stabilizer[j * 4+2] = 1
                stabilizer[j * 4 +3] = 1
        majorana_code.push(MajoranaOperator(1j, stabilizer))

    ##  添加额外的稳定子
    for i in range(pauli_code.N):
        stabilizer = [0] * (pauli_code.N * 4)
        stabilizer[i * 4] = 1
        stabilizer[i * 4+1]=1
        stabilizer[i * 4+2] = 1
        stabilizer[i * 4+3] = 1
        majorana_code.push(MajoranaOperator(1, stabilizer))
    return majorana_code