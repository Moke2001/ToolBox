import numpy as np
from tenpy import MPS
from Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Format.TermFormat.MultiTermFormat import MultiTermFormat
from Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy


class StateTenpy:
    def __init__(self, data):
        self.data = data

    def apply(self, term,model,normal=False):
        assert isinstance(model,ModelTenpy)
        if isinstance(term,OnsiteTermFormat):
            mps_index=model.lattice.lat2mps_idx(term.get_position())
            self.data.apply_local_op(mps_index, term.get_op(), unitary=None, renormalize=normal, cutoff=1e-13, understood_infinite=False)
        else:
            raise NotImplementedError


    def expectation(self, term, model):
        if isinstance(term,OnsiteTermFormat):
            mps_index = model.lattice.lat2mps_idx(term.get_position())
            return self.data.expectation_value(term.get_op(),[mps_index])
        elif isinstance(term,CouplingTermFormat):
            mps_index_0,mps_index_1 = model.lattice.lat2mps_idx(term.get_position())
            op_0,op_1=term.get_op()
            return self.data.expectation_value_term([(op_0,mps_index_0),(op_1,mps_index_1)])
        elif isinstance(term,MultiTermFormat):
            pass
        else:
            raise NotImplementedError


    def overlap(self, other):
        return self.data.overlap(other.data)

    def copy(self):
        return StateTenpy(self.data.copy())

    @staticmethod
    def get_product_state(model,state_array):
        assert isinstance(model, ModelTenpy)
        model.build_lattice()
        state = np.empty((model.get_site_number(),),dtype=int)
        for site_index, state_temp in np.ndenumerate(state_array):
            mps_index = model.lattice.lat2mps_idx(site_index)
            mps_index=int(mps_index)
            state[mps_index] = state_temp
        return StateTenpy(MPS.from_product_state(model.get_lattice().mps_sites(),state))

