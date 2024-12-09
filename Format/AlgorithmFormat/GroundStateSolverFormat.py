from abc import abstractmethod


class GroundStateSolverFormat:
    def __init__(self, model):
        self.model = model
        self.groundstate=None
        self.groundenergy=None

    @abstractmethod
    def compute(self):
        pass

    def get_result(self):
        return self.groundenergy, self.groundstate

