import numpy as np
from tenpy import Lattice
from TenpyBox.StateTenpy.StateTenpy import StateTenpy
from Format.LatticeFormat.LatticeFormat import LatticeFormat


class LatticeTenpy(LatticeFormat):
    def __init__(self):
        super().__init__()
        self.lattice = None


    def update_lattice(self, cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list):
        super().update_lattice(cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)


    def build(self):
        for i in range(self.get_site_number_in_one_cell()):
            self.inner_site_list[i].build()
        self.lattice = Lattice(self.cell_period_list, self.inner_site_list, basis=self.cell_vector_list, positions=self.inner_coordinate_list)


    def get_site(self, index_tuple):
        return self.lattice.get_site(index_tuple)


    def get_product_state(self, state_array):
        assert all(isinstance(it, int) for it in state_array)
        assert isinstance(self.lattice, Lattice)
        state=[]
        for site_index, state_temp in np.ndenumerate(state_array):
            mps_index=self.lattice.lat2mps_idx(site_index)
            state[mps_index] = state_temp
        return StateTenpy(state)

    def get_lattice(self):
        self.build()
        return self.lattice