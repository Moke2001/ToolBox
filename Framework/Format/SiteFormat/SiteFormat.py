import copy
from abc import abstractmethod
import numpy as np


class SiteFormat:
    # %%  BLOCK：构造函数
    """""
    SiteFormat：格式类格点对象
    self.dimension：格式类属性，int对象，格点局部Hilbert空间维度
    self.conserve：格式类属性，str对象，格点守恒物理量
    self.operator_dict：格式类属性，dict对象，格点上的局域算符的np.ndarray及其名称
    """""
    def __init__(self, dimension,conserve):
        assert isinstance(dimension, int), 'dimension必须是int对象'
        assert isinstance(conserve,str) or conserve is None,'conserve必须是str对象'
        self.dimension = dimension
        self.conserve = conserve
        self.operator_dict = {
            'identity': np.eye(dimension),  # 初始只包含单位算符
        }


    # %%  BLOCK：更改格点的守恒量
    """
    input.conserve：str对象，新的守恒量
    """
    def change_conserve(self, conserve):
        self.conserve = conserve


    # %%  BLOCK：推送新的算符
    """
    input.name：str对象，定义算符名称
    input.operator：np.ndarray对象，定义局域算符的矩阵形式
    添加对应的名称-矩阵键值对
    """
    def push_operator(self, name, operator):
        assert self.operator_dict.get(name, None) is None,'该名称算符已存在'
        assert isinstance(name,str),'name必须是str对象'
        assert isinstance(operator,np.ndarray),'operator必须是np.ndarray对象'
        assert self.get_dimension()==operator.shape[0]==operator.shape[1],'算符矩阵形状与格点Hilbert空间维度不匹配'
        self.operator_dict[name] = operator


    #%%  BLOCK：获取算符字典
    """
    output：dict对象，返回格点的局域算符名称-矩阵字典
    """
    def get_operator_dict(self):
        return self.operator_dict


    # %%  BLOCK：删除算符
    """
    input.name：str对象，算符名称
    删除对应的名称-矩阵键值对
    """
    def pop_operator(self, name):
        self.operator_dict.pop(name)


    # %%  BLOCK：复制函数
    """
    output：SiteFormat对象
    SiteFormat的复制函数
    """
    def copy(self):
        return copy.deepcopy(self)


    # %%  BLOCK：得到算符的矩阵形式
    """
    input.name：str对象，算符的名称
    output：np.ndarray对象，算符的矩阵形式
    """
    def get_operator(self, name):
        return self.operator_dict.get(name, None)


    #%%  BLOCK：返回格点局域Hilbert空间的维度
    """
    output：int对象，格点的Hilbert空间维度
    """
    def get_dimension(self):
        return self.dimension


    # %%  BLOCK：实例函数
    """
    根据格式类构造对应的数据类数据属性
    """
    @abstractmethod
    def build_site(self):
        pass
