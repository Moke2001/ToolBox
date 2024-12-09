import numpy as np
from qutip import *
from QutipBox.SiteQutip.SiteQutip import SiteQutip
from Format.LatticeFormat.LatticeFormat import LatticeFormat


class LatticeQutip(LatticeFormat):
    # %%  BLOCK：构造函数
    """""
    self.cell_period_list：格式类属性，元胞延展次数，形如[1,2,3]
    self.cell_vector_list：格式类属性，每个方向上的元胞基矢，形如[np.array,np.array]
    self.inner_site_list：格式类属性，元胞内Site对象列表，形如[Site,Site]
    self.inner_coordinate：格式类属性，元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：格式类属性，元胞个数
    self.space_dimension：格式类属性，空间维度数目
    self.site_number_in_one_cell：格式类属性，元胞中格点个数
    self.site_array：数据类属性，qutip的格点对象张量
    """""
    def __init__(self,lattice_format):
        super().__init__()
        cell_period_list=lattice_format.cell_period_list
        cell_vector_list=lattice_format.cell_vector_list
        inner_site_list=lattice_format.inner_site_list
        inner_coordinate_list=lattice_format.inner_coordinate_list
        self.update_lattice(cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)
        self.site_array=None


    # %%  BLOCK：构造数据类属性
    def build_lattice(self):
        for i in range(len(self.inner_site_list)):
            self.inner_site_list[i]=SiteQutip(self.inner_site_list[i])
            self.inner_site_list[i].build_site()

        self.site_array = np.empty(self.cell_period_list + [len(self.inner_site_list)], dtype=SiteQutip)
        for site_index, site_iteration in np.ndenumerate(self.site_array):
            self.site_array[site_index] = self.inner_site_list[site_index[-1]].copy()



    #%%  BLOCK：返回格点对象
    def get_site(self,index_tuple):
        return self.site_array[index_tuple]


    # %%  BLOCK：返回根据指定生成的qutip形式算符
    def get_operator_qutip(self,name,index_tuple):
        self.build_lattice()
        result = None
        index=np.ravel_multi_index(index_tuple, self.site_array.shape)
        for i in range(self.site_number):
            if i == 0:
                if index == i:
                    result = self.get_site(index_tuple).get_local_operator_qutip(name)
                else:
                    result = self.get_site(index_tuple).get_local_operator_qutip('identity')
            else:
                if index == i:
                    result = tensor(result, self.get_site(index_tuple).get_local_operator_qutip(name))
                else:
                    result = tensor(result, self.get_site(index_tuple).get_local_operator_qutip('identity'))
        return result


    #%%  BLOCK：返回lattice数据属性
    def get_lattice(self):
        return self.site_array

