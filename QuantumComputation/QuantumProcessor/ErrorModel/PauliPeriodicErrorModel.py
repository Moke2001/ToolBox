import itertools
from qutip import *
from QuantumComputation.QuantumProcessor.ErrorModel.UnitaryErrorModel import UnitaryErrorModel
from QuantumComputation.Helper.OperatorGenerator import operator_generator


class PauliPeriodicErrorModel(UnitaryErrorModel):
    #%%  USER：周期量子Pauli噪声模型生成函数
    """"
    self.N：int对象，局域个数
    self.error_number：int对象，错误qubits个数
    self.p：float对象，错误几率
    self.kraus_list：list of Qobj对象，Kraus算符集合
    """""
    def __init__(self,N,p):
        pauli_error_list = []
        probability_list=[]
        for i in range(1,N):
            pauli_ops = ['X', 'Y', 'Z']
            for i in range(self.N):
                error_list = []
                params = ()
                for j in range(i):
                    params = params + (pauli_ops,)
                for j in itertools.combinations(range(self.N), i):
                    error = ['I'] * self.N
                    for l in itertools.product(*params):
                        for k in range(len(j)):
                            error[j[k]] = l[k]
                        error_list.append(error.copy())
                for j in range(len(error_list)):
                    kraus_temp=1
                    for k in range(len(error_list[j])):
                        if error_list[j][k] == 'X':
                            kraus_temp = kraus_temp* operator_generator(self.N,sigmax(),k)
                        elif error_list[j][k] == 'Y':
                            kraus_temp = kraus_temp* operator_generator(self.N,sigmay(),k)
                        elif error_list[j][k] == 'Z':
                            kraus_temp = kraus_temp* operator_generator(self.N,sigmaz(),k)
                    pauli_error_list.append(kraus_temp)
                    p_temp=(p**i)*((1-p)**(N-i))
                    probability_list.append(p_temp)

        ##  给Kraus算符赋值
        super().__init__(N,pauli_error_list,probability_list)



