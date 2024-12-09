import random
from abc import abstractmethod

import numpy as np


class MeasurementSimulatorTenpy:
    def __init__(self, model, psi_initial, projector_list, eigenvalue_list):
        self.projector_list = projector_list
        self.eigenvalue_list = eigenvalue_list
        self.psi_initial = psi_initial
        self.psi_final = None
        self.model = model
        self.value=None

    @abstractmethod
    def compute(self):
        P_list = []
        for i in range(len(self.projector_list)):
            P_list.append(self.psi_initial.expectation(self.projector_list[i], self.model))
        index = random.choices(range(len(P_list)), weights=P_list, k=1)[0]
        psi_result = self.psi_initial.copy()
        self.psi_final = psi_result.apply(self.projector_list[index], self.model, normal=True)
        self.value = self.eigenvalue_list[index]

    def get_result(self):
        return self.value,self.psi_final