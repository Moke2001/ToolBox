##---Class Model in Qutip---##
from qutip import *
from QutipToolBox.Lattice.Lattice import Lattice


class Model():
    ##  Model类构造函数
    def __init__(self, lattice,operator_list):
        ##  参数检查与赋值
        assert isinstance(lattice,Lattice),'lattice must be a Lattice'
        assert isinstance(operator_list,list),'operator_list must be a list'
        self.lattice = lattice
        self.operator_list = operator_list

        ##  构造哈密顿量
        H=0
        for i in range(len(self.operator_list)):
            if len(self.operator_list[i]) == 2:
                H=H+self.operator_local_to_global(self.operator_list[i][0],self.operator_list[i][1])
            elif len(self.operator_list[i]) == 4:
                operator_0=self.operator_local_to_global(self.operator_list[i][0], self.operator_list[i][1])
                operator_1=self.operator_local_to_global(self.operator_list[i][2], self.operator_list[i][3])
                H=H+operator_0*operator_1
            else:
                raise ValueError('operator_list must have length 2 or 4')
        self.H = H

    ##  获取lattice
    def get_lattice(self):
        return self.lattice

    ##  获取算符的全局形式
    def operator_local_to_global(self,flag,operator):
        result=None
        index=self.get_lattice().get_site_index(flag)
        for i in range(self.get_lattice().site_number):
            if i == 0:
                if index==i:
                    result=operator
                else:
                    result=self.get_lattice().get_site(i).get_identity()
            else:
                if index==i:
                    result=tensor(result,operator)
                else:
                    result=tensor(result,self.get_lattice().get_site(i).get_identity())
        return result

    def get_product_state(self,state_list):
        psi=basis(self.lattice.get_site(0).dimension,state_list[0])
        for i in range(1,len(state_list)):
            psi=tensor(psi,basis(self.lattice.get_site(0).dimension,state_list[i]))
        return psi


