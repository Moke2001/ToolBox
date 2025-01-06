from sympy.strategies.branch import identity
from qutip import *
from QuantumComputation.QuantumProcessor.ErrorModel.UnitaryErrorModel import UnitaryErrorModel
from QuantumComputation.Helper.OperatorGenerator import operator_generator


class PauliGateErrorModel(UnitaryErrorModel):
    #%%  USER：量子Pauli逻辑门噪声模型生成函数
    """"
    self.N：int对象，局域个数
    self.probability：float对象，发生错误的几率
    """""
    def __init__(self, N, p, *args):
        ##  单一qubit的逻辑门上发生的错误
        if len(args)==1:
            error_list = []
            error_list.append(operator_generator(N, identity(2),args[0]))
            error_list.append(operator_generator(N, sigmax(),args[0]))
            error_list.append(operator_generator(N, sigmay(),args[0]))
            error_list.append(operator_generator(N, sigmaz(),args[0]))
            probability_list = [1 - 3 * p, p, p, p]
            super().__init__(N,error_list,probability_list)

        ##  两个qubits的逻辑门发生的噪声
        elif len(args)==2:
            II=operator_generator(N, identity(2),args[0])*operator_generator(N, identity(2),args[1])
            IX=operator_generator(N, identity(2),args[0])*operator_generator(N, sigmax(),args[1])
            IY=operator_generator(N, identity(2),args[0])*operator_generator(N, sigmay(),args[1])
            IZ=operator_generator(N, identity(2),args[0])*operator_generator(N, sigmaz(),args[1])
            XI=operator_generator(N, sigmax(),args[0])*operator_generator(N, identity(2),args[1])
            XX=operator_generator(N, sigmax(),args[0])*operator_generator(N, sigmax(),args[1])
            XY=operator_generator(N, sigmax(),args[0])*operator_generator(N, sigmay(),args[1])
            XZ=operator_generator(N, sigmax(),args[0])*operator_generator(N, sigmaz(),args[1])
            YI=operator_generator(N, sigmay(),args[0])*operator_generator(N, identity(2),args[1])
            YX=operator_generator(N, sigmay(),args[0])*operator_generator(N, sigmax(),args[1])
            YY=operator_generator(N, sigmay(),args[0])*operator_generator(N, sigmay(),args[1])
            YZ=operator_generator(N, sigmay(),args[0])*operator_generator(N, sigmaz(),args[1])
            ZI=operator_generator(N, sigmaz(),args[0])*operator_generator(N, identity(2),args[1])
            ZX=operator_generator(N, sigmaz(),args[0])*operator_generator(N, sigmax(),args[1])
            ZY=operator_generator(N, sigmaz(),args[0])*operator_generator(N, sigmay(),args[1])
            ZZ=operator_generator(N, sigmaz(),args[0])*operator_generator(N, sigmaz(),args[1])
            error_list=[II,IX,IY,IZ,XI,XX,XY,XZ,YI,YX,YY,YZ,ZI,ZX,ZY,ZZ]
            probability_list = [(1-3*p)*(1-3*p)]+[p*(1-3*p)]*4+[p*p]*3+[p*(1-3*p)]+[p*p]*3+[p*(1-3*p)]+[p*p]*3
            super().__init__(N,error_list,probability_list)
