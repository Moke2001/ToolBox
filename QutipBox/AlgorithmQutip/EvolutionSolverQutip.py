from abc import abstractmethod

from qutip import mesolve

from Format.AlgorithmFormat.EvolutionSolverFormat import EvolutionSolverFormat


class EvolutionSolverQutip(EvolutionSolverFormat):
    def __init__(self,model,psi_initial,expectation_terms,t_list):
        super().__init__(model,psi_initial,expectation_terms,t_list)


    @abstractmethod
    def compute(self):
        H_list,C_list,N_list,function_params=self.model.get_model()
        result_list = mesolve(H_list, rho0=self.psi_initial, tlist=self.t_list, c_ops=C_list, e_ops=self.expectation_terms, args=function_params).expect
        psi_result = mesolve(H_list, rho0=self.psi_initial, tlist=self.t_list, c_ops=C_list, args=function_params).states[-1]
        for i in range(len(result_list)):
            self.data_list[i]=result_list[i]
        self.psi_final=psi_result


    def get_result(self):
        return self.data_list,self.psi_final