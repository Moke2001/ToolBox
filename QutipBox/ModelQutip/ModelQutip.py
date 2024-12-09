import uuid
import numpy as np
from Format.ModelFormat.ModelFormat import ModelFormat
from Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Format.TermFormat.MultiTermFormat import MultiTermFormat
from Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Format.TermFormat.OverallOnsiteTermFormat import OverallOnsiteTermFormat
from QutipBox.ModelQutip.Function import Function
from QutipBox.LatticeQutip.LatticeQutip import LatticeQutip


class ModelQutip(ModelFormat,LatticeQutip):
    # %%  BLOCK：构造函数
    """""
    Qutip数据类：模型对象，定义哈密顿量，多重继承
    self.H：数据类属性，qutip算符形式的静态哈密顿量
    self.H_list：数据类属性，qutip算符形式列表的哈密顿量列表
    self.C_list：数据类属性，qutip算符形式列表的Lindblad算符列表
    self.N_list：数据类属性，qutip算符形式列表的噪声算符列表
    self.function_params：数据类属性，含时算符的函数参数列表
    self.site_array：数据类属性，qutip格点对象张量
    self.terms：格式类属性，list of Term对象，储存模型的作用量
    self.number：格式类属性，int对象，储存作用量个数
    self.cell_period_list：格式类属性，元胞延展次数，形如[1,2,3]
    self.cell_vector_list：格式类属性，每个方向上的元胞基矢，形如[np.array,np.array]
    self.inner_site_list：格式类属性，元胞内Site对象列表，形如[Site,Site]
    self.inner_coordiante：格式类属性，元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：格式类属性，元胞个数
    self.space_dimension：格式类属性，空间维度数目
    self.site_number_in_one_cell：格式类属性，元胞中格点个数
    """""
    def __init__(self,model_format):
        ModelFormat.__init__(self)
        LatticeQutip.__init__(self,model_format)
        self.terms=model_format.terms.copy()
        self.number=model_format.number
        self.H = None
        self.H_list = []
        self.C_list = []
        self.N_list = []
        self.function_params = {}


    #%%  BLOCK：构造数据类属性
    def build(self):
        LatticeQutip.build_lattice(self)
        ##  遍历作用量列表
        self.H = 0
        self.H_list = []
        self.C_list = []
        self.N_list = []
        for term_temp in self.terms:

            ##  单局域作用量
            if isinstance(term_temp, OnsiteTermFormat):
                index_tuple = term_temp.get_position()
                name = term_temp.get_op()
                operator = self.get_operator_qutip(name, index_tuple)

            ##  单两体相互作用量
            elif isinstance(term_temp, CouplingTermFormat):
                index_tuple_0, index_tuple_1 = term_temp.get_position()
                name_0, name_1 = term_temp.get_op()
                operator_0 = self.get_operator_qutip(name_0, index_tuple_0)
                operator_1 = self.get_operator_qutip(name_1, index_tuple_1)
                operator = operator_0 * operator_1

            ##  多体相互作用量
            elif isinstance(term_temp, MultiTermFormat):
                index_tuple_list = term_temp.get_position()
                name_list = term_temp.get_op()
                assert len(index_tuple_list) == len(name_list)
                operator = None
                for i in range(len(index_tuple_list)):
                    if i == 0:
                        operator = self.get_operator_qutip(name_list[i], index_tuple_list[i])
                    else:
                        operator = operator * self.get_operator_qutip(name_list[i], index_tuple_list[i])

            ##  遍历局域相互作用量
            elif isinstance(term_temp, OverallOnsiteTermFormat):
                operator = 0
                for index_tuple, site_iteration in np.ndenumerate(self.site_array):
                    if index_tuple[-1] == term_temp.get_unit():
                        operator = operator + self.get_operator_qutip(term_temp.get_op(), index_tuple)

            ##  不支持其他作用量形式
            else:
                raise TypeError

            ##  含时演化
            if term_temp.time:
                function = term_temp.function
                function_params = term_temp.function_params
                uuid_temp = uuid.uuid1()
                self.function_params[uuid_temp] = function_params
                function_temp = Function(function, uuid_temp)
                if term_temp.effect == 'hamiltonian':
                    self.H_list.append([operator, function_temp.MyFunction])
                elif term_temp.effect == 'lindbladian':
                    self.C_list.append([operator, function_temp.MyFunction])
                elif term_temp.effect == 'noise':
                    self.N_list.append([operator, function_temp.MyFunction])
                else:
                    raise TypeError

            ##  不含时演化
            else:
                strength = term_temp.strength
                if term_temp.effect == 'hamiltonian':
                    self.H = self.H + operator * strength
                elif term_temp.effect == 'lindbladian':
                    self.C_list.append(operator * strength)
                elif term_temp.effect == 'noise':
                    self.N_list.append(operator * strength)
                else:
                    raise TypeError

        ##  将静态哈密顿量添加到列表中
        self.H_list = [self.H] + self.H_list


    #%%  BLOCK：返回用于计算的模型对象
    def get_model(self):
        self.build()
        return self.H_list,self.C_list,self.N_list,self.function_params
