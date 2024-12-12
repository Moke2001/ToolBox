import numpy as np
from Framework.Format.SiteFormat.SiteFormat import SiteFormat


class SpinHalfSiteFormat(SiteFormat):
    # %%  BLOCK：构造函数
    """""
    SpinHalfSiteFormat：格式类1/2自旋格点对象
    self.dimension：格式类属性，int对象，格点局部Hilbert空间维度
    self.conserve：格式类属性，str对象，格点守恒物理量
    self.operator_dict：格式类属性，dict对象，格点上的局域算符的np.ndarray及其名称
    添加了所有的Pauli算符
    """""
    def __init__(self,conserve):
        super().__init__(2,conserve)
        self.push_operator('sigmax', np.array([[0,1],[1,0]],dtype=complex))
        self.push_operator('sigmay', np.array([[0,-1j],[1j,0]],dtype=complex))
        self.push_operator('sigmaz', np.array([[1,0],[0,-1]],dtype=complex))
        self.push_operator('sigmaup', np.array([[1,0],[0,0]],dtype=complex))
        self.push_operator('sigmadown', np.array([[0,0],[0,1]],dtype=complex))
        self.push_operator('sigmaplus', np.array([[0,1],[0,0]],dtype=complex))
        self.push_operator('sigmaminus', np.array([[0,0],[1,0]],dtype=complex))


