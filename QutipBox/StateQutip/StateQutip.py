import numpy as np
from Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Format.TermFormat.MultiTermFormat import MultiTermFormat
from Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Format.TermFormat.OverallOnsiteTermFormat import OverallOnsiteTermFormat
from QutipBox.ModelQutip.ModelQutip import ModelQutip


class StateQutip:
    def __init__(self,data):
        self.data = data

    def apply(self,term,model,normal=False):
        if normal:
            self.data=StateQutip.get_operator_qutip(term,model)*self.data
            self.data=self.data/self.data.norm()
        else:
            self.data = StateQutip.get_operator_qutip(term, model) * self.data


    def expectation(self,term,model):
        op=StateQutip.get_operator_qutip(term,model)
        return self.data.dag()*op*self.data

    def overlap(self,other):
        return other.dag()*self.data

    @ staticmethod
    def get_operator_qutip(term,model):
        assert isinstance(model,ModelQutip)
        assert term.time==False
        if isinstance(term, OnsiteTermFormat):
            index_tuple = term.get_position()
            name = term.get_op()
            operator = model.get_operator_qutip(name, index_tuple)*term.get_strength()

        ##  单两体相互作用量
        elif isinstance(term, CouplingTermFormat):
            index_tuple_0, index_tuple_1 = term.get_position()
            name_0, name_1 = term.get_op()
            operator_0 = model.get_operator_qutip(name_0, index_tuple_0)
            operator_1 = model.get_operator_qutip(name_1, index_tuple_1)
            operator = operator_0 * operator_1*term.get_strength()

        ##  多体相互作用量
        elif isinstance(term, MultiTermFormat):
            index_tuple_list = term.get_position()
            name_list = term.get_op()
            assert len(index_tuple_list) == len(name_list)
            operator = None
            for i in range(len(index_tuple_list)):
                if i == 0:
                    operator = model.get_operator_qutip(name_list[i], index_tuple_list[i])*term.get_strength()
                else:
                    operator = operator * model.get_operator_qutip(name_list[i], index_tuple_list[i])*term.get_strength()

        ##  遍历局域相互作用量
        elif isinstance(term, OverallOnsiteTermFormat):
            operator = 0
            for index_tuple, site_iteration in np.ndenumerate(model.site_array):
                if index_tuple[-1] == term.get_unit():
                    operator = operator + model.get_operator_qutip(term.get_op(), index_tuple)
            operator = operator*term.get_strength()

        ##  不支持其他作用量形式
        else:
            raise TypeError

        return operator

    def copy(self):
        return StateQutip(self.data.copy())
