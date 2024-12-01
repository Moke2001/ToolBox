##---Class Site in Qutip---##
import numpy as np
from qutip import *

class Site:
    ##  Site类构造函数
    def __init__(self,location,dimension):
        assert isinstance(location,tuple),'location must be a tuple'
        assert isinstance(dimension,int),'dimension must be a int'
        self.location = location
        self.dimension = dimension

    ##  重载相等运算符
    def __eq__(self, other):
        assert isinstance(other,Site),'Other must be a Site'
        return self.location == other.location and self.dimension == other.dimension

    ##  重载输出运算符
    def __str__(self):
        print('This site has a location:')
        print(self.location)
        print('This site has a dimension:')
        print(self.dimension)

    ##  获取Site上的单位算符
    def get_identity(self):
        return identity(self.dimension)

    ##  获取Site的坐标
    def get_location(self):
        return self.location

    ##  计算两个Site之间的距离
    @ classmethod
    def distance(cls,site_0,site_1):
        assert isinstance(site_0,Site),'Site_0 must be a Site'
        assert isinstance(site_1,Site),'Site_1 must be a Site'
        assert len(site_0.location) == len(site_1.location),'Two sites must have the same location dimension'
        result=0
        for i in range(len(site_0.location)):
            result=result+(site_0.location[i]-site_1.location[i])**2
        return np.sqrt(result)
