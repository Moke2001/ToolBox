from abc import abstractmethod


class MeasurementSimulatorFormat:
    def __init__(self, model, psi_initial, projector_list, eigenvalue_list):
        self.projector_list = projector_list
        self.eigenvalue_list = eigenvalue_list
        self.psi_initial = psi_initial
        self.psi_final = None
        self.model = model
        self.value=None

    @abstractmethod
    def compute(self):
        pass

    def get_result(self):
        return self.value,self.psi_final