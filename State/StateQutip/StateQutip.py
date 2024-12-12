import copy
import numpy as np
from qutip import Qobj
from State.StateNumpy.StateNumpy import StateNumpy


class StateQutip:
    #%%  USER：构造函数
    def __init__(self,*args):
        ##  SECTION：空构造函数---------------------------------------------------------------------
        if len(args) == 0:
            self.vector=None
            self.dimension_array=None

        ##  SECTION：转换构造函数-------------------------------------------------------------------
        elif len(args) == 1 and isinstance(args[0], StateNumpy):
            self.vector=Qobj(args[0].tensor.reshape((np.prod(args[0].tensor.shape),1)),dims=[list(args[0].tensor.shape),[1]*len(args[0].tensor.shape)])
            self.dimension_array=args[0].dimension_array

        ##  SECTION：标准构造函数-------------------------------------------------------------------
        elif len(args) == 2 and isinstance(args[0], Qobj) and isinstance(args[1], np.ndarray):
            self.vector=args[0]
            self.dimension_array=args[1]

        ##  SECTION：其他构造函数-------------------------------------------------------------------
        else:
            raise NotImplemented


    # %%  USER：重载加法
    def __add__(self, other):
        assert isinstance(other, StateQutip)
        return StateQutip(self.vector+other.vector,self.dimension_array)


    # %%  USER：重载减法
    def __sub__(self, other):
        assert isinstance(other,StateQutip)
        return StateQutip(self.vector-other.vector,self.dimension_array)


    # %%  USER：重载数乘
    def __mul__(self, other):
        assert isinstance(other, complex) or isinstance(other, float) or isinstance(other, int)
        return StateQutip(self.vector * other, self.dimension_array)


    # %%  USER：重载数乘
    def __rmul__(self, other):
        return self.__mul__(other)


    # %%  USER：重载数除
    def __truediv__(self, other):
        assert isinstance(other, complex) or isinstance(other, float) or isinstance(other, int)
        return StateQutip(self.vector*(1/other), self.dimension_array)


    # %%  USER：计算模长
    def norm(self):
        return self.vector.norm()


    # %%  USER：归一化
    def normalize(self):
        self.vector=self.vector/self.norm()


    # %%  KEY：复制函数
    def copy(self):
        return copy.deepcopy(self)

