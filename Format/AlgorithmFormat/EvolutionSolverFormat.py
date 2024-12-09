from abc import abstractmethod


class EvolutionSolverFormat:
    def __init__(self,model,psi_initial,expectation_terms,t_list):
        self.expectation_terms = expectation_terms
        self.data_list=[]
        self.psi_initial = psi_initial
        self.psi_final = None
        self.model = model
        self.t_list = t_list

    @abstractmethod
    def compute(self):
        pass


    def get_result(self):
        return self.data_list,self.psi_final