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
        assert isinstance(dimension, int), 'dimension必须是一个int对象'
        self.dimension = dimension
        self.conserve = conserve
        self.operator_dict = {
            'identity': np.eye(dimension),  # 初始只包含单位算符
        }


    # %%  BLOCK：推送新的算符
    def push_operator(self, name, operator):
        term = self.operator_dict.get(name, None)
        if term is None:
            self.operator_dict[name] = operator
        else:
            raise ValueError('Operator ' + name + ' already defined')


    #%%  BLOCK：获取算符字典
    def get_operator_dict(self):
        return self.operator_dict


    # %%  BLOCK：删除算符
    def pop_operator(self, name):
        self.operator_dict.pop(name)


    # %%  BLOCK：复制函数
    def copy(self):
        result = SiteFormat(self.dimension,self.conserve)
        result.operator_dict = self.operator_dict.copy()
        return result


    # %%  BLOCK：得到算符
    def get_operator(self, name):
        return self.operator_dict.get(name, None)


    #%%  BLOCK：返回维度
    def get_dimension(self):
        return self.dimension


    # %%  BLOCK：实例函数
    @abstractmethod
    def build_site(self):
        pass
