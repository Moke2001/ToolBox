from abc import abstractmethod
from Format.AlgorithmFormat.EnergySpectrumSolverFormat import EnergySpectrumSolverFormat


class EnergySpectrumSolverQutip(EnergySpectrumSolverFormat):
    def __init__(self,model):
        super().__init__(model)


    @abstractmethod
    def compute(self):
        eigenvalues, eigenvectors = self.model.H.eigenstates()
        self.eigenenergies=eigenvalues
        self.eigenstates=eigenvectors


    def get_result(self):
        return self.eigenenergies, self.eigenstates