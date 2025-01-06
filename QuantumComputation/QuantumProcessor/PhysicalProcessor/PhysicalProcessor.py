from abc import abstractmethod
from random import choices
import numpy as np


class PhysicalProcessor:
    def __init__(self,number_locality):
        self.N = number_locality

    @abstractmethod
    def initialize(self,method):
        pass

    @abstractmethod
    def gate(self,*args):
        pass

    @abstractmethod
    def measure(self,*args):
        pass

    @abstractmethod
    def get_error(self,name,*args):
        pass

    """
    control格式：
    Gate：(gate_name:str,*index,*parameters)
    Measure：(measure_name:str,*index,*parameters) or (measure_name:str,operator_string)
    Feedback：(feedback_name:str,control_measure_list,feedback_list)
    """
    def execute(self,state,rho,control):
        ##  测量指令
        if control[0][0:7] == "Measure":
            eigenvalues, eigenstates = self.measure(control)
            P_list = []
            for i in range(len(eigenvalues)):
                P = eigenstates[i].dag() * state * eigenstates[i]
                P_list.append(np.abs(P))
            index = choices(range(len(P_list)), weights=P_list, k=1)[0]
            projector = eigenstates[index] * eigenstates[index].dag()
            rho = (1 / P_list[index]) * projector * rho * projector
            state = projector * state
            state = state / state.norm()
            kraus_list = self.get_error(*control).kraus_list
            for j in range(len(kraus_list)):
                rho = kraus_list[j] * rho * kraus_list[j].dag()

        ##  反馈指令
        elif control[0][0:8] == "Feedback":
            control_measure_list = control[1]
            decoder = control[2]
            syndrome_list=[]
            for i in range(len(control_measure_list)):
                eigenvalues, eigenstates = self.measure(*control_measure_list[i])
                P_list = []
                for j in range(len(eigenvalues)):
                    P = eigenstates[j].dag() * state * eigenstates[j]
                    P_list.append(np.abs(P))
                index = choices(range(len(P_list)), weights=P_list, k=1)[0]
                projector = eigenstates[index] * eigenstates[index].dag()
                rho = (1 / P_list[index]) * projector * rho * projector
                state = projector * state
                state = state / state.norm()
                kraus_list = self.get_error(*control).kraus_list
                for j in range(len(kraus_list)):
                    rho = kraus_list[j] * rho * kraus_list[j].dag()
                syndrome_list.append(eigenvalues[index])
            control_gate_list=decoder(control_measure_list,syndrome_list)
            for i in range(len(control_gate_list)):
                state,rho=self.execute(state,rho,control_gate_list[i])

        ##  量子逻辑门指令
        else:
            rho = self.gate(*control) * rho * self.gate(*control).dag()
            state = self.gate(*control) * state
            kraus_list = self.get_error(*control).kraus_list
            for j in range(len(kraus_list)):
                rho = kraus_list[j] * rho * kraus_list[j].dag()

        ##  返回结果
        return state,rho


    #%%  USER：执行某个指令串
    def circuit(self,control):
        ##  初始化
        start_state = control[0]
        state = self.initialize(start_state)
        rho = state * state.dag()

        ##  执行指令
        for i in range(1, len(control)):
            state,rho=self.execute(state,rho,control[i])

        ##  计算保真度并返回结果
        fidelity = np.sqrt(state.dag() * rho * state)
        return state, rho, fidelity