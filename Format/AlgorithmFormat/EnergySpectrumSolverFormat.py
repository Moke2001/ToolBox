from abc import abstractmethod



class EnergySpectrumSolverFormat():
    def __init__(self, model):
        self.model = model
        self.eigenenergies = []
        self.eigenstates = []

    @abstractmethod
    def compute(self):
        pass

    def get_result(self):
        return self.eigenenergies, self.eigenstates


