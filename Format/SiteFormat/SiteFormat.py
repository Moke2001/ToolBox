from abc import abstractmethod

import numpy as np


class SiteFormat:
    # %%  BLOCK：构造函数
    def __init__(self, dimension):
        assert isinstance(dimension, int), 'dimension must be a int'
        self.dimension = dimension
        self.operator_dict = {
            'identity': np.eye(dimension),
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
        result = SiteFormat(self.dimension)
        result.operator_dict = self.operator_dict.copy()
        return result


    # %%  BLOCK：得到算符
    def get_operator(self, name):
        return self.operator_dict.get(name, None)


    #%%  BLOCK：返回维度
    def get_dimension(self):
        return self.dimension
