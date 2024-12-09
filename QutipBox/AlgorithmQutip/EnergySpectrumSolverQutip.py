from abc import abstractmethod
from Format.AlgorithmFormat.EnergySpectrumSolverFormat import EnergySpectrumSolverFormat
from Format.ModelFormat.ModelFormat import ModelFormat
from QutipBox.ModelQutip.ModelQutip import ModelQutip


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


    def build(self):
        if isinstance(self.model,ModelFormat):
            self.model=ModelQutip(self.model)
        elif isinstance(self.model,ModelQutip):
            pass
        else:
            raise TypeError