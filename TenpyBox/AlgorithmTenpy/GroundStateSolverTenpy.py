from abc import abstractmethod
import numpy as np
from tenpy.algorithms import dmrg
from Format.ModelFormat.ModelFormat import ModelFormat
from TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy


class GroundStateSolverTenpy:
    def __init__(self, model):
        self.model = model
        self.groundstate=None
        self.groundenergy=None


    @abstractmethod
    def compute(self,chi_max):
        state_array=self.model.get_structure(self,int)
        for site_index, state_temp in np.ndenumerate(state_array):
            state_array[site_index]=0
        psi = self.model.get_product_state(self, state_array)
        dmrg_params = {
            'mixer': None,
            'max_E_err': 1.e-10,
            'trunc_params': {
                'chi_max': chi_max,
                'svd_min': 1.e-10
            },
            'combine': True
        }
        info = dmrg.run(psi, self.model.get_model(), dmrg_params)  # the main work...
        return info['E'], psi

    def build(self):
        if isinstance(self.model,ModelFormat):
            self.model=ModelTenpy(self.model)
        elif isinstance(self.model,ModelTenpy):
            pass
        else:
            raise TypeError

    def get_result(self):
        return self.groundenergy, self.groundstate