from abc import abstractmethod

import numpy as np

from Format.SiteFormat.SiteFormat import SiteFormat


class SpinHalfSiteFormat(SiteFormat):
    # %%  BLOCK：构造函数
    def __init__(self):
        super().__init__(2)
        self.push_operator('sigmax', np.array([[0,1],[1,0]],dtype=complex))
        self.push_operator('sigmay', np.array([[0,-1j],[1j,0]],dtype=complex))
        self.push_operator('sigmaz', np.array([[1,0],[0,-1]],dtype=complex))
        self.push_operator('sigmaup', np.array([[1,0],[0,0]],dtype=complex))
        self.push_operator('sigmadown', np.array([[0,0],[0,1]],dtype=complex))
        self.push_operator('sigmaplus', np.array([[0,1],[0,0]],dtype=complex))
        self.push_operator('sigmauminus', np.array([[0,0],[1,0]],dtype=complex))

    #%%  BLOCK：实例函数
    @abstractmethod
    def build(self):
        pass
