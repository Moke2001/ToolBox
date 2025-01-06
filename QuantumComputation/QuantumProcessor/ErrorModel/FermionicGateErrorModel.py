from QuantumComputation.QuantumProcessor.ErrorModel.UnitaryErrorModel import UnitaryErrorModel
from QuantumComputation.Helper.OperatorGenerator import operator_generator
from qutip import *

class FermionicGateErrorModel(UnitaryErrorModel):
    #%%  USER：量子Fermionic逻辑门的量子噪声的生成函数
    """"
    self.N：int对象，局域个数
    self.p：float对象，发生错误的几率
    self.kraus_list：list of Qobj对象，由参数生成的噪声操作集合
    """""
    def __init__(self,N,p,*args):
        ##  单个site逻辑门的噪声
        if len(args)==1:
            I = operator_generator(N, identity(2), 0)
            A = fcreate(N, args[0]) + fdestroy(N, args[0])
            B = 1j * (fdestroy(N, args[0]) - fcreate(N, args[0]))
            C = A * B
            error_list=[I,A,B,C]
            probability_list=[1-3*p,p,p,p]
            super().__init__(N,error_list,probability_list)

        ##  两个sites逻辑门的噪声
        elif len(args)==2:
            I0 = operator_generator(N, identity(2), 0)
            A0 = fcreate(N, args[0]) + fdestroy(N, args[0])
            B0 = 1j * (fdestroy(N, args[0]) - fcreate(N, args[0]))
            C0 = A0 * B0
            A1 = fcreate(N, args[1]) + fdestroy(N, args[1])
            B1 = 1j * (fdestroy(N, args[1]) - fcreate(N, args[1]))
            C1 = A1 * B1
            error_list = [I0,A1,B1,C1,A0,A0*A1,A0*B1,A0*C1,B0,B0*A1,B0*B1,B0*C1,C0,C0*A1,C0*B1,C0*C1]
            probability_list = [(1 - 3 * p) * (1 - 3 * p)] + [p * (1 - 3 * p)] * 4 + [p * p] * 3 + [p * (1 - 3 * p)] + [p * p] * 3 + [p * (1 - 3 * p)] + [p * p] * 3
            super().__init__(N,error_list,probability_list)