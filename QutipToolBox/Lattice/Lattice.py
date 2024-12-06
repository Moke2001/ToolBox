import numpy as np
from QutipToolBox.Site.Site import Site
from qutip import *


class Lattice:
    #%%  BLOCK：构造函数
    """""
    self.Ls：元胞延展次数，形如[1,2,3]
    self.unit_vectors：每个方向上的元胞基矢，形如[np.array,np.array]
    self.cell_sites：元胞内Site对象列表，形如[Site,Site]
    self.cell_vectors：元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：元胞个数
    self.space_dimension：空间维度数目
    self.site_number_in_one_cell：元胞中格点个数
    self.sites：系统格点数组
    """""
    def __init__(self, Ls, unit_vectors, cell_sites, cell_vectors ):
        assert len(Ls) == len(unit_vectors)
        assert len(cell_sites) == len(cell_vectors)
        assert all(it.shape[0]==len(unit_vectors) for it in unit_vectors)
        self.Ls = Ls
        self.cell_number=np.prod(Ls)
        self.space_dimension=len(unit_vectors)
        self.site_number_in_one_cell=len(cell_sites)
        self.site_number = self.site_number_in_one_cell*self.cell_number
        self.sites=np.empty(Ls+[len(cell_sites)],dtype=Site)
        for site_index,site_iteration in np.ndenumerate(self.sites):
            self.sites[site_index]=cell_sites[site_index[-1]].copy()
        self.unit_vectors = unit_vectors
        self.cell_vectors = cell_vectors


    #%%  BLOCK：获得格点坐标
    def get_location(self,position):
        result=np.zeros(self.space_dimension)
        for i in range(self.space_dimension):
            result=result+self.unit_vectors[i]*position[i]
        return result


    #%%  BLOCK：获得Site对象
    def get_site(self, position):
        return self.sites[position]


    #%%  BLOCK：求Site间的距离
    def get_distance(self,position_0,position_1):
        location_0=self.get_location(position_0)
        location_1=self.get_location(position_1)
        return np.linalg.norm(location_0-location_1)


    #%%  BLOCK：返回局域算符全局形式
    def get_operator(self,name,position):
        index=0
        result=None
        for i in range(len(position)):
            index=index+position[i]*sum((self.Ls+[self.site_number_in_one_cell])[0:i])
        for i in range(self.site_number):
            if i==0:
                if index==i:
                    result=self.get_site(position).get_operator(name)
                else:
                    result=self.get_site(position).get_operator('identity')
            else:
                if index == i:
                    result = tensor(result,self.get_site(position).get_operator(name))
                else:
                    result=tensor(result,self.get_site(position).get_operator('identity'))
        return result


    # %%  BLOCK：获得直积态
    def get_product_state(self, state_tensor):
        state=None
        for site_index, site_iteration in np.ndenumerate(self.sites):
            if state is None:
                state=basis(site_iteration.dimension,state_tensor[site_index])
            else:
                state=tensor(state,basis(site_iteration.dimension,state_tensor[site_index]))
        return state