from Physics.QuantumComputation.Encoder.Code.ClassicalCode.RegularCode import RegularCode
from Project.FermionicLDPCCode.Main.Majorana2Css import majorana2css
from Project.FermionicLDPCCode.Main.Pauli2Majorana import pauli2majorana
from Project.FermionicLDPCCode.Main.PauliHypergraphProductCode import pauli_hypergraph_product_code
from Project.FermionicLDPCCode.Main.Css2Fermi import css2majorana

if __name__ == '__main__':
    # s_0 = MajoranaGroup(1,[0,0,0,0,0,0,1,0,1,0,1,0,1,0])
    # s_1 = MajoranaGroup(1, [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0])
    # s_2 = MajoranaGroup(1, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0])
    # s_3 = MajoranaGroup(1,[0,0,0,0,0,0,0,1,0,1,0,1,0,1])
    # s_4 = MajoranaGroup(1, [0, 0, 0,1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1])
    # s_5 = MajoranaGroup(1, [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1])
    # majorana_code=MajoranaCode([s_0,s_1,s_2,s_3,s_4,s_5])
    regular_code = RegularCode(12)
    pauli_code = pauli_hypergraph_product_code(regular_code)
    majorana_code = pauli2majorana(pauli_code)
    pauli_code=majorana2css(majorana_code)
    majorana_code=css2majorana(pauli_code)
    print(len(majorana_code.get_logical_operator()))
    pass