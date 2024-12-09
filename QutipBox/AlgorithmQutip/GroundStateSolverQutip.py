from abc import abstractmethod


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