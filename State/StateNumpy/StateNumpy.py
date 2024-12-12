import copy
import numpy as np
from State.StateNumpy.LocalStateNumpy import LocalStateNumpy


class StateNumpy:
    #%%  USER：构造函数
    def __init__(self,*args):
        ##  SECTION：空构造函数---------------------------------------------------------------------
        if len(args) == 0:
            self.tensor=None
            self.dimension_array=None

        ##  SECTION：次标准构造函数-----------------------------------------------------------------
        elif  all(isinstance(it,np.ndarray) for it in args) and all(it.dtype == LocalStateNumpy for it in args):
            dimension_array=[]
            for index_tuple, state_local_temp in np.ndenumerate(args[0]):
                assert isinstance(state_local_temp,LocalStateNumpy)
                dimension_array.append(state_local_temp.get_dimension())
            self.dimension_array=dimension_array
            self.tensor=None
            for i in range(len(args)):
                tensor_temp=None
                for index_tuple, state_local_temp in np.ndenumerate(args[i]):
                    assert isinstance(state_local_temp,LocalStateNumpy)
                    if tensor_temp is None:
                        tensor_temp=state_local_temp.get_amount_array()
                    else:
                        tensor_temp=np.einsum('...,i->...i',tensor_temp,state_local_temp.get_amount_array())
                if self.tensor is None:
                    self.tensor=tensor_temp
                else:
                    self.tensor=self.tensor+tensor_temp

        ##  SECTION：标准构造函数-------------------------------------------------------------------
        elif len(args) == 2 and isinstance(args[0], np.ndarray) and isinstance(args[1], np.ndarray):
            flag=0
            for index_tuple, state_local_temp in np.ndenumerate(args[1]):
                assert args[1][index_tuple].get_dimension==args[0].shape[flag]
                flag=flag+1
            self.tensor=args[0]
            self.dimension_array=args[1]

        ##  SECTION：复制构造函数-------------------------------------------------------------------
        elif len(args)==1 and isinstance(args[0], StateNumpy):
            self.dimension_array=args[0].get_dimension().copy()
            self.tensor=args[0].get_tensor().copy()

        ##  SECTION：无效构造函数-------------------------------------------------------------------
        else:
            raise NotImplemented


    #%%  USER：重载加法
    def __add__(self,other):
        assert isinstance(other,StateNumpy)
        assert self.dimension_array==other.dimension_array
        return StateNumpy(self.tensor + other.tensor,self.dimension_array)


    # %%  USER：重载减法
    def __sub__(self,other):
        assert isinstance(other,StateNumpy)
        assert self.dimension_array==other.dimension_array
        return StateNumpy(self.tensor - other.tensor,self.dimension_array)


    # %%  USER：重载数乘
    def __mul__(self,other):
        assert isinstance(other,complex) or isinstance(other,float) or isinstance(other,int)
        return StateNumpy(self.tensor * other, self.dimension_array)


    # %%  USER：重载数乘
    def __rmul__(self,other):
        return self.__mul__(other)


    # %%  USER：重载数除
    def __truediv__(self, other):
        assert isinstance(other, complex) or isinstance(other, float) or isinstance(other, int)
        return StateNumpy(self.tensor / other, self.dimension_array)


    # %%  KEY：复制函数
    def copy(self):
        return copy.deepcopy(self)
