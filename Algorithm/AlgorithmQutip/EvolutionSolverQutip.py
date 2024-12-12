import numpy as np
from Data.State.State import State
from Data.StateVectorTools.Term2Qobj import term2qobj
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.TermFormat.TermFormat import TermFormat
from Framework.Format.TermFormat.TermsFormat import TermsFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer
from qutip import *


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
def evolution_solver_qutip(model_origin:ModelFormat,psi_origin:State,expectation_terms:list,t_list:np.ndarray):
    ##  标准化
    assert isinstance(t_list,np.ndarray),'参数t_list必须是np.ndarray对象'
    assert isinstance(psi_origin,State),'参数psi_origin必须是State对象'
    assert isinstance(model_origin,ModelFormat),'参数model_origin必须是ModelFormat对象'
    assert isinstance(expectation_terms,list),'参数expectation_terms必须是list对象'
    model=model_preparer(model_origin,'qutip')
    psi_origin.validate(model,'vector')

    ##  求可观测量的qutip形式算符
    E_list=[]
    for i in range(len(expectation_terms)):
        if isinstance(expectation_terms[i],TermFormat):
            E_list.append(term2qobj(model,expectation_terms[i]))
        elif isinstance(expectation_terms[i],TermsFormat):
            E_list.append(term2qobj(model,expectation_terms[i]))

    ##  用qutip计算
    H_list, C_list, N_list, function_params = model.get_model()
    result_list = mesolve(H_list, rho0=psi_origin.vector, tlist=t_list, c_ops=C_list, e_ops=E_list, args=function_params).expect
    psi_result = mesolve(H_list, rho0=psi_origin.vector, tlist=t_list, c_ops=C_list, args=function_params).states[-1]

    ##  期望序列赋值
    data_list=[]
    for i in range(len(result_list)):
        data_list.append(result_list[i])

    ##  态矢赋值
    state_result=State()
    state_result.initial(psi_result)

    ##  返回结果
    return state_result,data_list
