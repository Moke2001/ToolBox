from abc import abstractmethod


class EnergySpectrumSolverTenpy():
    def __init__(self, model):
        self.model = model
        self.eigenenergies = []
        self.eigenstates = []

    @abstractmethod
    def compute(self):
        pass

    def get_result(self):
        return self.eigenenergies, self.eigenstates