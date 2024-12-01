import numpy as np
from QutipToolBox.Model.Model import Model


def energy_spectrum(model):
    assert isinstance(model,Model),'model must be an instance of Model'
    eigenvalues, eigenvectors = model.H.eigenstates()
    return eigenvalues, eigenvectors