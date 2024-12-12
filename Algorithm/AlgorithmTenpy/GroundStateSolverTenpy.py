import numpy as np
from tenpy import MPS
from tenpy.algorithms import dmrg
from Data.State.State import State
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
ground_state_solver_qutip：计算基态能量和基态态矢
input.model_origin：ModelFormat对象，算符所在的模型
output.groundenergy：float对象，基态能量
output.groundstate：State对象，基态态矢
influence：本函数不改变参数对象
"""
def ground_state_solver_tenpy(model_origin)->tuple[float, State]:
    ##  标准化
    assert isinstance(model_origin,ModelFormat),'参数model_origin必须是ModelFormat对象'
    model=model_preparer(model_origin,'qutip')

    ##  DMRG算法参数
    dmrg_params = {
        'mixer': None,
        'max_E_err': 1.e-10,
        'trunc_params': {
            'chi_max': model.get_site_number()*5,
            'svd_min': 1.e-10
        },
        'combine': True
    }

    ##  算法计算
    psi=MPS.from_product_state(model.get_lattice().mps_sites(),[0]*model.get_site_number())
    info = dmrg.run(psi, model.get_model(), dmrg_params)
    psi_final=State()
    psi_final.initial(psi)

    ##  返回结果
    return np.real(info['E']), psi_final
