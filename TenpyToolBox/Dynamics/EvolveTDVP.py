from tenpy import MPS
from tenpy.algorithms import tdvp
from TenpyToolBox.ModelPackage.ModelPackage import ModelPackage


#%%  BLOCK：执行TDVP算法计算演化后的态矢
"""
输入量：总时间，时间分段数，截断维度，初态态矢，模型
输出量：末态态矢
"""
def evolve_tdvp(time_total:float, N_step:int, chi_max:int, psi_origin:MPS, model:ModelPackage):
    ##  TDVP执行参数
    tdvp_params = {
        'start_time': 0,  # 起始时间
        'dt': time_total/N_step,  # 分割时间
        'N_steps': N_step,  # 分割数目
        'trunc_params': {
            'chi_max': chi_max,  # 截断维度
            'svd_min': 1.e-10,  # SVD允差
            'trunc_cut': None
        }
    }
    
    ##  执行TDVP算法
    psi_result=psi_origin.copy()  # 拷贝MPS对象
    tdvp_engine = tdvp.TimeDependentTwoSiteTDVP(psi_result, model.get_model(), tdvp_params)  # 生成TDVP对象
    tdvp_engine.run()  # 计算
    
    ##  返回结果
    return psi_result