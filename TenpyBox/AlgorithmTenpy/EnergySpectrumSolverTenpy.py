from abc import abstractmethod

from Format.ModelFormat.ModelFormat import ModelFormat
from TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy


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

    def build(self):
        if isinstance(self.model,ModelFormat):
            self.model=ModelTenpy(self.model)
        elif isinstance(self.model,ModelTenpy):
            pass
        else:
            raise TypeError