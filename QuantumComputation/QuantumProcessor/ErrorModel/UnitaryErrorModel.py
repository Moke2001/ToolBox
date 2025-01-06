import numpy as np

from QuantumComputation.QuantumProcessor.ErrorModel.ErrorModel import ErrorModel


class UnitaryErrorModel(ErrorModel):
    #%%  USER：量子幺正噪声模型生成函数
    """"
    self.N：int对象，局域个数
    error_list：list of Qobj对象，幺正算符集合
    probability_list：list of float对象，发生对应幺正错误的几率
    """""
    def __init__(self,N,error_list,probability_list):
        ##  标准化
        assert len(error_list) == len(probability_list),'噪声数目和几率数目需要匹配'
        assert np.isclose(np.sum(probability_list),1,1e-5,1e-5),'几率需要归一化'

        ##  赋值
        self.error_list = error_list
        self.probability_list = probability_list

        ##  计算对应的Kraus操作集合
        kraus_list=[]
        for i in range(len(self.error_list)):
            kraus_list.append(np.sqrt(self.probability_list[i])*self.error_list[i])
        super().__init__(N,kraus_list)

