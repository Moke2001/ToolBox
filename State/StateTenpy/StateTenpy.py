import copy
import numpy as np
from tenpy import Array, LegCharge, MPS
import Algorithm.Interface.InterfaceTenpy.GetLatticeTenpy
from State.StateNumpy.StateNumpy import StateNumpy
from Format.ModelFormat.ModelFormat import ModelFormat


class StateTenpy:
    # %%  USER：构造函数
    def __init__(self,*args):
        ##  SECTION：空构造函数---------------------------------------------------------------------
        if len(args) == 0:
            self.mps=None
            self.dimension_array=None

        ##  SECTION：标准构造函数-------------------------------------------------------------------
        elif len(args) == 2 and isinstance(args[0], StateNumpy) and isinstance(args[1], ModelFormat):
            leg_list=[]
            label_list=[]
            flag=0
            for index_temp,ignore in np.ndenumerate(args[1].get_dimension_array()):
                site_temp=args[1].get_site(index_temp)
                leg_list.append(LegCharge.from_trivial(site_temp.get_dimension()))
                label_list.append('p'+str(flag))
                flag=flag+1
            temp=Array.from_ndarray(args[0].tensor,leg_list,labels=label_list)
            self.mps=MPS.from_full(Algorithm.Interface.InterfaceTenpy.GetLatticeTenpy.get_lattice_tenpy(args[1]).mps_sites(),temp)
            self.dimension_array=args[1].get_dimension_array()

        ##  SECTION：标准构造函数-------------------------------------------------------------------
        elif len(args) == 2 and isinstance(args[0], MPS) and isinstance(args[1],np.ndarray):
            self.mps=args[0]
            self.dimension_array=args[1]

        ##  SECTION：其他构造函数-------------------------------------------------------------------
        else:
            raise NotImplemented


    # %%  USER：重载加法
    def __add__(self, other):
        assert isinstance(other, StateTenpy)
        return StateTenpy(self.mps.add(other.mps,1,1),self.dimension_array)


    # %%  USER：重载减法
    def __sub__(self, other):
        assert isinstance(other,StateTenpy)
        return StateTenpy(self.mps.add(other.mps,1,-1),self.dimension_array)


    # %%  USER：重载数乘
    def __mul__(self, other):
        assert isinstance(other, complex) or isinstance(other, float) or isinstance(other, int)
        return StateTenpy(self.mps.add(self.mps,0,other),self.dimension_array)


    # %%  USER：重载数乘
    def __rmul__(self, other):
        return self.__mul__(other)


    # %%  USER：重载除法
    def __truediv__(self, other):
        assert isinstance(other, complex) or isinstance(other, float) or isinstance(other, int)
        return StateTenpy(self.mps.add(self.mps,0,1/other),self.dimension_array)


    # %%  USER：计算模长
    def norm(self):
        return self.mps.norm


    # %%  USER：归一化
    def normalize(self):
        self.mps.canonical_form()


    # %%  KEY：复制函数
    def copy(self):
        return copy.deepcopy(self)


