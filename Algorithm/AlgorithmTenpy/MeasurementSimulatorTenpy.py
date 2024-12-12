import random
from Data.State.State import State
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
measurement_simulator_qutip：计算态矢测量结果与坍缩态
input.model_origin：ModelFormat对象，算符所在的模型
input.psi_origin：State对象，初始态矢
input.projector_list：list of TermFormat对象，投影算符
input.eigenvalue_list：list of float对象，投影算符对应测量值
output.psi_final：State对象，测量后坍缩到的态矢
output.value：float对象，测量值
influence：本函数不改变参数对象
"""
def measurement_simulator_tenpy(model_origin, psi_origin, projector_list, eigenvalue_list)->tuple[float,State]:
    ##  标准化
    assert isinstance(psi_origin, State), '参数psi_origin必须是State对象'
    assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
    assert isinstance(projector_list, list),'参数projector_list必须是list对象'
    assert isinstance(eigenvalue_list, list),'参数eigenvalue_list必须是list对象'
    model = model_preparer(model_origin, 'tenpy')

    ##  随机坍缩模拟
    P_list = []
    for i in range(len(projector_list)):
        P_list.append(psi_origin.expectation(model, projector_list[i]))
    index = random.choices(range(len(P_list)), weights=P_list, k=1)[0]
    psi_final = psi_origin.copy()
    psi_final.apply(projector_list[index], model, True, 'mps')
    value = eigenvalue_list[index]

    ##  返回结果
    return value, psi_final

