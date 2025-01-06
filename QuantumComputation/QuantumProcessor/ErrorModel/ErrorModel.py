from qutip import *
from QuantumComputation.Helper.OperatorGenerator import operator_generator
import numpy as np


class ErrorModel:
    #%%  USER：量子噪声模型生成函数
    """"
    self.N：int对象，局域个数
    kraus_list：list of Qobj对象，Kraus算符集合
    """""
    def __init__(self,N,kraus_list):
        self.N = N

        ##  验证Kraus算符满足归一化条件
        check=0
        for error in kraus_list:
            check=check+error.dag()*error
        if np.isclose((check-operator_generator(N,identity(2),0)).norm(),0,1e-5,1e-5):
            self.kraus_list = kraus_list
        else:
            raise ValueError('Kraus算符不归一化')
