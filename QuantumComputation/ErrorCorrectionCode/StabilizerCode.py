import itertools
from abc import abstractmethod


class StabilizerCode:
    # %% USER：构造函数
    """"
    self.N：int对象，局域个数
    self.stabilizers：list of Operator对象，稳定子生成元
    self.weight：int对象，编码能纠正的错误的最大权重
    """""
    def __init__(self,N):
        self.N = N
        self.stabilizers = []
        self.weight=None


    # %%  USER：推送稳定子
    """
    input.stabilizers：object对象，要推送的稳定子
    influence：本函数将self.stabilizers添加一个稳定子
    """
    def push(self,stabilizer):
        self.stabilizers.append(stabilizer)
        self.weight = None

    #%%  USER：撤销稳定子
    """
    input.index：int对象，要撤销的稳定子的序号
    influence：本函数将self.stabilizers[index]删除
    """
    def pop(self,index):
        self.stabilizers.pop(index)
        self.weight = None


    #%%  USER：计算编码率
    @abstractmethod
    def get_ratio(self):
        return (self.N-len(self.stabilizers))/self.N


    #%%  USER：计算能纠正的最大错误
    @abstractmethod
    def get_weight(self):
        pass