from Project.FermionicLDPCCode.Map.Css2Fermi import css2fermi
from Project.FermionicLDPCCode.Map.Majorana2Css import majorana2css
from Project.FermionicLDPCCode.Map.Pauli2Majorana import pauli2majorana


def map_chain(pauli_code):
    print('当前代码是：Pauli code')
    print('它的纠错距离是：' + str(pauli_code.get_weight()))
    print('它的物理比特数是：' + str(pauli_code.N))
    print('它的逻辑比特数是：' + str(pauli_code.N - len(pauli_code.stabilizers)))
    print('')

    majorana_code=pauli2majorana(pauli_code)
    print('当前代码是：Majorana code')
    print('它的纠错距离是：' + str(majorana_code.get_weight()))
    print('它的物理比特数是：' + str(majorana_code.N))
    print('它的逻辑比特数是：' + str(majorana_code.N - len(majorana_code.stabilizers)))
    print('')

    css_code=majorana2css(majorana_code)
    print('当前代码是：CSS code')
    print('它的纠错距离是：' + str(css_code.get_weight()))
    print('它的物理比特数是：' + str(css_code.N))
    print('它的逻辑比特数是：' + str(css_code.N - len(css_code.stabilizers)))
    print('')

    fermionic_code=css2fermi(css_code)
    print('当前代码是：Fermionic code')
    print('它的纠错距离是：' + str(fermionic_code.get_weight()))
    print('它的物理比特数是：' + str(fermionic_code.N))
    print('它的逻辑比特数是：' + str(fermionic_code.N - len(fermionic_code.stabilizers)))
    print('')
