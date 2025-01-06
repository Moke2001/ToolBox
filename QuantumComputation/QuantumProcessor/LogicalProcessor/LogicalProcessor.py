from abc import abstractmethod, abstractstaticmethod
import numpy as np


class LogicalProcessor:
    def __init__(self,physics_circuit):
        self.physical_processor = physics_circuit
        self.logical_states=[]

    @abstractstaticmethod
    def decoder(control_measure_list,syndrome_list):
        pass

    @abstractmethod
    def initializer(self,method):
        pass

    @abstractmethod
    def compiler(self,control_logical):
        pass

    def execute(self,state,rho,control_logical):
        control=self.compiler(*control_logical)
        return self.physical_processor.execute(state,rho,control)

    def circuit(self,control_logical_list):
        state=self.initializer(control_logical_list[0])
        rho=state*state.dag()
        for i in range(1,len(control_logical_list)):
            state,rho=self.execute(state,rho,control_logical_list[i])
        fidelity = np.sqrt(state.dag() * rho * state)
        return state,rho,fidelity

