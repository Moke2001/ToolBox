from Project.FermionicLDPCCode.Main.MapChain import map_chain
from QuantumComputation.ErrorCorrectionCode.PauliStabilizerCode.PauliOperator import PauliOperator
from QuantumComputation.ErrorCorrectionCode.PauliStabilizerCode.PauliStabilizerCode import PauliStabilizerCode


if __name__ == '__main__':
    pauli_code = PauliStabilizerCode(5)
    pauli_code.push(PauliOperator(1,['X', 'Z', 'Z', 'X', 'I']))
    pauli_code.push(PauliOperator(1,['I', 'X', 'Z', 'Z', 'X']))
    pauli_code.push(PauliOperator(1,['X', 'I', 'X', 'Z', 'Z']))
    pauli_code.push(PauliOperator(1,['Z', 'X', 'I', 'X', 'Z']))

    map_chain(pauli_code)