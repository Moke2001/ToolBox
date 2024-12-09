from abc import abstractmethod

from Format.ModelFormat.ModelFormat import ModelFormat
from QutipBox.ModelQutip.ModelQutip import ModelQutip


class GroundStateSolverQutip:
    def __init__(self, model):
        self.model = model
        self.groundstate=None
        self.groundenergy=None

    @abstractmethod
    def compute(self):
        H_list,C_list,N_list,function_params=self.model.get_model()
        groundenergy, groundstate=H_list[0].groundstate()
        self.groundenergy=groundenergy
        self.groundstate=groundstate

    def get_result(self):
        return self.groundenergy, self.groundstate


    def build(self):
        if isinstance(self.model,ModelFormat):
            self.model=ModelQutip(self.model)
        elif isinstance(self.model,ModelQutip):
            pass
        else:
            raise TypeError