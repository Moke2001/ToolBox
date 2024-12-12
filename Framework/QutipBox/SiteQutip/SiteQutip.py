import copy

from Framework.Format.SiteFormat.SiteFormat import SiteFormat
from qutip import *


class SiteQutip(SiteFormat):
    #%%  BLOCK：构造函数
    """""
    Qutip数据类：格点对象，定义局部格点Hilbert空间和局域算符及其名称
    self.operator_dict：格式类属性，局域算符字典
    self.dimension：格式类属性，维度
    self.operator_dict_qutip：数据类属性，qutip形式局域算符字典
    """""
    def __init__(self,site_format):
        assert isinstance(site_format,SiteFormat)
        super().__init__(site_format.dimension,site_format.conserve)
        self.operator_dict=site_format.operator_dict.copy()
        self.operator_dict_qutip=self.operator_dict.copy()


    #%%  BLOCK：构造数据类属性qutip算符字典
    def build_site(self):
        for key in self.get_operator_dict():
            self.operator_dict_qutip[key]=Qobj(self.get_operator_dict()[key])


    #%%  BLOCK：返回qutip算符类型
    def get_local_operator_qutip(self,key):
        self.build_site()
        return self.operator_dict_qutip.get(key)


    #%%  BLOCK：返回qutip算符字典
    def get_site(self):
        self.build_site()
        return self.operator_dict_qutip

    #%% BLOCK：复制函数
    def copy(self):
        return copy.deepcopy(self)