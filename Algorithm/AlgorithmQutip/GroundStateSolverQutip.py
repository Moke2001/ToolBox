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
def ground_state_solver_qutip(model_origin:ModelFormat)->tuple[float,State]:
    ##  标准化
    assert isinstance(model_origin,ModelFormat),'参数model_origin必须是ModelFormat对象'
    model=model_preparer(model_origin,'qutip')

    ##  计算
    H_list,C_list,N_list,function_params=model.get_model()
    groundenergy, temp=H_list[0].groundstate()
    groundstate=State()
    groundstate.initial(temp)

    ##  返回结果
    return groundenergy, groundstate