from abc import abstractmethod

import numpy as np
from tenpy.algorithms import tdvp


class EvolutionSolverTenpy:
    def __init__(self,model,psi_initial,expectation_terms,t_list):
        self.expectation_terms = expectation_terms
        self.data_list=[]
        self.psi_initial = psi_initial
        self.psi_final = None
        self.model = model
        self.t_list = t_list

    @abstractmethod
    def compute(self,N_step,chi_max):
        psi_result = self.psi_initial.copy()  # 拷贝MPS对象
        for i in range(len(self.expectation_terms)):
            self.data_list.append(np.array([self.psi_initial.expectation(self.expectation_terms[i],self.model)]))
        for i in range(self.t_list.shape[0]):
            tdvp_params = {
                'start_time': self.t_list[i],  # 起始时间
                'dt': (self.t_list[i+1]-self.t_list[i])/N_step,  # 分割时间
                'N_steps': N_step,  # 分割数目
                'trunc_params': {
                    'chi_max': chi_max,  # 截断维度
                    'svd_min': 1.e-10,  # SVD允差
                    'trunc_cut': None
                }
            }

            ##  执行TDVP算法
            tdvp_engine = tdvp.TimeDependentTwoSiteTDVP(psi_result, self.model.get_model(), tdvp_params)  # 生成TDVP对象
            tdvp_engine.run()  # 计算
            for j in range(len(self.expectation_terms)):
                self.data_list[i]=np.append(self.data_list[j],np.array([psi_result.expectation(self.expectation_terms[j], self.model)]))
        self.psi_final = psi_result


    def get_result(self):
        return self.data_list,self.psi_final