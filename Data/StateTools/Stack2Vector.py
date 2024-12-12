import numpy as np
from qutip import basis, tensor
from Data.LocalState.LocalState import LocalState
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
stack2vector：stack格式转化为vector数据
input.model_origin：ModelFormat对象，算符所在的模型
input.stack：list of np.ndarray对象，存储求和的直积态
output.vector：Qobj对象，vector数据
influence：本函数不改变参数对象
"""
def stack2vector(model_origin:ModelFormat,stack:list):
    ##  标准化
    assert isinstance(model_origin,ModelFormat),'参数model_origin必须是ModelFormat对象'
    assert isinstance(stack,list),'参数stack必须是list对象'
    assert all(isinstance(it,np.ndarray) for it in stack),'参数stack内数据必须是np.ndarray对象'
    model=model_preparer(model_origin,'qutip')
    assert all(model.get_lattice().shape==it.shape for it in stack),'参数stack格式必须与model晶格格式匹配'

    ##  对stack遍历每个直积态
    vector=0
    for i in range(len(stack)):
        state_array_temp =stack[i]  # 当前待加入的直积态
        vector_temp =None  # 当前直积态对应的vector数据初始化

        ##  对直积态每个位点遍历
        for index_tuple_temp, state_local_temp in np.ndenumerate(state_array_temp):
            assert isinstance(state_local_temp,LocalState),'参数stack内np.ndarray必须存储LocalState对象'
            vector_local_temp = 0  # 当前位点的vector数据初始化

            ##  对格点上的每个基矢乘以系数求和
            for j in range(state_local_temp.get_dimension()):
                vector_local_temp =vector_local_temp+basis(state_local_temp.get_dimension() ,j ) *state_local_temp[j]

            ##  将格点vector做张量积
            if vector_temp is None:
                vector_temp =vector_local_temp
            else:
                vector_temp =tensor(vector_temp ,vector_local_temp)

        ##  对直积态求和
        vector =vector+vector_temp

    ##  返回结果
    return vector