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
    def __init__(self):
        ModelFormat.__init__(self)
        LatticeQutip.__init__(self)
        self.H = None
        self.H_list = []
        self.C_list = []
        self.N_list = []
        self.function_params = {}

    def build(self):
        LatticeQutip.build(self)
        ##  遍历作用量列表
        self.H = 0
        self.H_list = []
        self.C_list = []
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

    def get_model(self):
        return self.H_list,self.C_list,self.N_list,self.function_params
