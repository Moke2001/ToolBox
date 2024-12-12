import copy
import numpy as np


class SiteFormat:
    # %%  USER：构造函数
    """""
    SiteFormat：格式类格点对象
    self.dimension：格式类属性，int对象，格点局部Hilbert空间维度
    self.conserve：格式类属性，str对象，格点守恒物理量
    self.operator_dict：格式类属性，dict对象，格点的局域算符的np.ndarray及其名称
    """""
    def __init__(self,*args):
        ##  SECTION：复制构造函数-------------------------------------------------------------------
        if len(args)==1 and isinstance(args[0], SiteFormat):
            self.dimension = args[0].get_dimension()  # 格式属性：局域Hilbert空间维度
            self.conserve = args[0].get_conserve()  # 格式属性：守恒量
            self.operator_dictionary = args[0].get_operator_dictionary()  # 格式属性：算符字典


        #%%  SECTION：标准构造函数------------------------------------------------------------------
        elif len(args)==2 and isinstance(args[0],int):
            self.dimension = args[0]  # 格式属性：局域Hilbert空间维度
            self.conserve = args[1]  # 格式属性：守恒量
            self.operator_dictionary = {'identity': np.eye(self.dimension),}  # 格式属性：算符字典


    # %%  USER：添加对应的名称-矩阵键值对
    """
    input.name：str对象，定义算符名称
    input.operator：np.ndarray对象，定义局域算符的矩阵形式
    influence：本程序改变self.dict，添加self.dict[name]=input.operator键值对
    """
    def push_operator(self, name:str, operator:np.ndarray):
        ##  标准化
        assert self.operator_dictionary.get(name, None) is None, '该名称算符已存在'
        assert isinstance(name,str),'参数name必须是str对象'
        assert isinstance(operator,np.ndarray),'参数operator必须是np.ndarray对象'
        assert self.get_dimension()==operator.shape[0]==operator.shape[1],'算符矩阵形状与格点Hilbert空间维度必须匹配'

        ##  推入新算符
        self.operator_dictionary[name] = operator


    # %%  USER：删除算符
    """
    input.name：str对象，算符名称
    influence：删除self.dict[name]键值对
    """
    def pop_operator(self, name:str):
        self.operator_dictionary.pop(name)


    #%%  KEY：返回格点局域Hilbert空间的维度
    """
    output：int对象，格点的Hilbert空间维度
    influence：本函数不改变参数对象
    """
    def get_dimension(self)->int:
        return self.dimension


    #%%  KEY：获取算符字典
    """
    output：dict对象，返回格点的局域算符名称-矩阵字典
    """
    def get_operator_dictionary(self)->dict:
        return self.operator_dictionary


    #%%  KEY：获取守恒量
    """
    output：str对象，返回格点守恒量名称
    """
    def get_conserve(self)->str:
        return self.conserve


    # %%  KEY：复制函数
    """
    output：SiteFormat对象，与self相同的属性
    influence：本函数不改变参数对象
    """
    def copy(self)->'SiteFormat':
        return copy.deepcopy(self)


    #%%  USER：实现一个SpinHalfSite
    """
    input.consever：str对象，守恒量
    output：SiteFormat对象，添加相应的算符
    influence：本函数不改变参数对象
    """
    @staticmethod
    def SpinHalfSiteFormat(conserve):
        site=SiteFormat(2,conserve)
        site.push_operator('sigmax', np.array([[0,1],[1,0]],dtype=complex))
        site.push_operator('sigmay', np.array([[0,-1j],[1j,0]],dtype=complex))
        site.push_operator('sigmaz', np.array([[1,0],[0,-1]],dtype=complex))
        site.push_operator('sigmaup', np.array([[1,0],[0,0]],dtype=complex))
        site.push_operator('sigmadown', np.array([[0,0],[0,1]],dtype=complex))
        site.push_operator('sigmaplus', np.array([[0,1],[0,0]],dtype=complex))
        site.push_operator('sigmaminus', np.array([[0,0],[1,0]],dtype=complex))
        return site