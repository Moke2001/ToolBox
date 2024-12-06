import uuid
import numpy as np
from QutipToolBox.Model.Function import Function
from Framework.Term.CouplingTerm import CouplingTerm
from Framework.Term.OnsiteTerm import OnsiteTerm
from Framework.Term.OverallOnsiteTerm import OverallOnsiteTerm
from Framework.Term.Terms import Terms


class Model(Terms):
    #%%  BLOCK：构造函数
    def __init__(self):
        super().__init__()
        self.lattice=None
        self.terms=[]
        self.H=None
        self.H_list=[]
        self.C_list=[]
        self.function_params={}


    #%%  BLOCK：晶格初始化
    def lattice_build(self,lattice):
        self.lattice=lattice


    #%%  BLOCK：构造模型的哈密顿量
    def build(self):
        ##  遍历作用量列表
        self.H=0
        self.H_list=[]
        self.C_list=[]
        for term_temp in self.terms:

            ##  单局域作用量
            if isinstance(term_temp, OnsiteTerm):
                position=term_temp.get_position()
                name=term_temp.get_op()
                operator = self.lattice.get_operator(name, position)

            ##  单两体相互作用量
            elif isinstance(term_temp, CouplingTerm):
                position_0,position_1=term_temp.get_position()
                name_0,name_1=term_temp.get_op()
                operator_0 = self.lattice.get_operator(name_0, position_0)
                operator_1 = self.lattice.get_operator(name_1, position_1)
                operator = operator_0 * operator_1

            ##  多体相互作用量
            elif isinstance(term_temp, CouplingTerm):
                position_list = term_temp.get_position()
                name_list = term_temp.get_op()
                assert len(position_list) == len(name_list)
                operator = None
                for i in range(len(position_list)):
                    if i == 0:
                        operator = self.lattice.get_operator(name_list[i], position_list[i])
                    else:
                        operator = operator * self.lattice.get_operator(name_list[i], position_list[i])

            ##  遍历局域相互作用量
            elif isinstance(term_temp, OverallOnsiteTerm):
                operator=0
                for site_index,site_iteration in np.ndenumerate(self.lattice.sites):
                    if site_index[-1]==term_temp.get_unit():
                        operator = operator + self.lattice.get_operator(term_temp.get_op(), site_index)

            ##  不支持其他作用量形式
            else:
                raise TypeError

            ##  含时演化
            if term_temp.time:
                function = term_temp.function
                function_params = term_temp.function_params
                uuid_temp=uuid.uuid1()
                self.function_params[uuid_temp]=function_params
                function_temp=Function(function,uuid_temp)
                if term_temp.effect=='hamiltonian':
                    self.H_list.append([operator,function_temp.MyFunction])
                elif term_temp.effect=='lindbladian':
                    self.C_list.append([operator,function_temp.MyFunction])
                elif term_temp.effect=='noise':
                    pass
                else:
                    raise TypeError

            ##  不含时演化
            else:
                strength = term_temp.strength
                if term_temp.effect=='hamiltonian':
                    self.H=self.H+operator*strength
                elif term_temp.effect=='lindbladian':
                    self.C_list.append(operator*strength)
                elif term_temp.effect=='noise':
                    pass
                else:
                    raise TypeError

        ##  将静态哈密顿量添加到列表中
        self.H_list=[self.H]+self.H_list


    #%%  BLOCK：获取lattice
    def get_lattice(self):
        return self.lattice


    # %%  BLOCK：获得格点坐标
    def get_location(self, position):
        return self.get_lattice().get_location(position)


    # %%  BLOCK：获得Site对象
    def get_site(self, position):
        return self.get_lattice().get_site(position)


    # %%  BLOCK：求Site间的距离
    def get_distance(self, position_0, position_1):
        return self.get_lattice().get_distance(position_0, position_1)


    # %%  BLOCK：返回局域算符全局形式
    def get_operator(self, name, position):
        return self.get_lattice().get_operator(name, position)


    # %%  BLOCK：获得直积态
    def get_product_state(self, state_list):
        return self.get_lattice().get_product_state(state_list)

    #%%  BLOCK：获得模型哈密顿量
    def get_H(self):
        self.build()
        return self.H_list


    #%%  BLOCK：获得模型Lindblad算符
    def get_C(self):
        self.build()
        return self.C_list


    #%%  BLOCK：获得模型参数
    def get_function_params(self):
        self.build()
        return self.function_params