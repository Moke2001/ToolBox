import numpy as np
from tenpy.algorithms import tdvp
from Data.State.State import State
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
energy_spectrum_solver_qutip：计算本征值和本征矢
input.model_origin：ModelFormat对象，算符所在的模型
input.psi_origin：State对象，初始态矢
input.expectation_terms：list of TermFormat对象，待求期望的可观测量
input.t_list：np.ndarray对象，时间序列
output.psi_final：State对象，末态态矢
output.data_list：list of np.ndarray对象，各个可观测量期望随时间变化，与t_list对应
influence：本函数不改变参数对象
"""
def evolution_solver_tenpy(model_origin:ModelFormat,psi_origin:State,expectation_terms:list,t_list:np.ndarray):
    ##  标准化
    assert isinstance(t_list,np.ndarray),'参数t_list必须是np.ndarray对象'
    assert isinstance(psi_origin,State),'参数psi_origin必须是State对象'
    assert isinstance(model_origin,ModelFormat),'参数model_origin必须是ModelFormat对象'
    assert isinstance(expectation_terms,list),'参数expectation_terms必须是list对象'
    model=model_preparer(model_origin,'tenpy')
    psi_origin.validate(model,'mps')

    ##  如果需要求可观测量期望
    if expectation_terms:
        data_list=[]
        psi_final=psi_origin.copy()
        ##  计算可观测量初始值
        for i in range(len(expectation_terms)):
            data_list.append(np.array([psi_final.expectation(model,expectation_terms[i])]))

        ##  计算可观测量含时演化
        for i in range(t_list.shape[0]-1):
            tdvp_params = {
                'start_time': t_list[i],  # 起始时间
                'dt': (t_list[i+1]-t_list[i])/np.max([model.get_site_number(),5]),  # 分割时间
                'N_steps': int(np.max([model.get_site_number(),5])),  # 分割数目
                'trunc_params': {
                    'chi_max': int(model.get_site_number()*3),  # 截断维度
                    'svd_min': 1.e-10,  # SVD允差
                    'trunc_cut': None
                }
            }

            ##  执行TDVP算法
            tdvp_engine = tdvp.TimeDependentTwoSiteTDVP(psi_final.mps, model.get_model(), tdvp_params)  # 生成TDVP对象
            tdvp_engine.run()  # 计算
            for j in range(len(expectation_terms)):
                data_list[j]=np.append(data_list[j],np.array([psi_final.expectation(model,expectation_terms[j])]))
            print('已完成：'+str(i/(t_list.shape[0])))
        return psi_final, data_list

    ##  如果不需要求可观测量期望
    else:
        psi_final = psi_origin.copy()
        tdvp_params = {
            'start_time': t_list[0],  # 起始时间
            'dt': t_list[1]-t_list[0],  # 分割时间
            'N_steps': t_list.shape[0],  # 分割数目
            'trunc_params': {
                'chi_max': int(model.get_site_number() * 3),  # 截断维度
                'svd_min': 1.e-10,  # SVD允差
                'trunc_cut': None
            }
        }
        tdvp_engine = tdvp.TimeDependentTwoSiteTDVP(psi_final.mps, model.get_model(), tdvp_params)  # 生成TDVP对象
        tdvp_engine.run()  # 计算
        return psi_final
