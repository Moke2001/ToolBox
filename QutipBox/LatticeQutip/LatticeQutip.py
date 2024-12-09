import numpy as np
from qutip import *

from QutipBox.StateQutip.StateQutip import StateQutip
from Format.LatticeFormat.LatticeFormat import LatticeFormat
from QutipToolBox.Site.Site import Site


class LatticeQutip(LatticeFormat):
    def __init__(self):
        super().__init__()
        self.site_array=None

    def update_lattice(self,cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list):
        super().update_lattice(cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)


    def build(self):
        if self.cell_period_list is not None:
            self.site_array = np.empty(self.cell_period_list + [len(self.inner_site_list)], dtype=Site)
            for site_index, site_iteration in np.ndenumerate(self.site_array):
                self.site_array[site_index] = self.inner_site_list[site_index[-1]].copy()
        else:
            raise ValueError


    def get_site(self,index_tuple):
        return self.site_array[index_tuple]


    def get_product_state(self,state_array):
        assert state_array.shape == self.site_array.shape
        assert all(isinstance(it,int) for it in state_array)
        state=None
        for site_index, state_temp in np.ndenumerate(state_array):
            if state is None:
                state=basis(self.site_array[site_index].get_dimension(),state_temp)
            else:
                state=tensor(state,basis(self.site_array[site_index].get_dimension(),state_temp))
        return StateQutip(state)


    def get_operator_qutip(self,name,index_tuple):
        index = 0
        result = None
        for i in range(len(index_tuple)):
            index = index + index_tuple[i] * sum((self.cell_period_list + [self.site_number_in_one_cell])[0:i])
        for i in range(self.site_number):
            if i == 0:
                if index == i:
                    result = self.get_site(index_tuple).get_operator(name)
                else:
                    result = self.get_site(index_tuple).get_operator('identity')
            else:
                if index == i:
                    result = tensor(result, self.get_site(index_tuple).get_operator(name))
                else:
                    result = tensor(result, self.get_site(index_tuple).get_operator('identity'))
        return result

    def get_lattice(self):
        return self.site_array

