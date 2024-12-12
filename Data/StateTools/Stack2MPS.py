import numpy as np
from tenpy import MPS
from Data.LocalState.LocalState import LocalState
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
stack2mps：stack格式转化为MPS数据
input.model_origin：ModelFormat对象，算符所在的模型
input.stack：list of np.ndarray对象，存储求和的直积态
output.mps：MPS对象，MPS数据
influence：本函数不改变参数对象
"""
def stack2mps(model_origin ,stack):
    ##  标准化
    assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
    assert isinstance(stack, list), '参数stack必须是list对象'
    assert all(isinstance(it, np.ndarray) for it in stack), '参数stack内数据必须是np.ndarray对象'
    model = model_preparer(model_origin, 'tenpy')

    ##  对stack遍历每个直积态
    mps =None
    for i in range(len(stack)):
        state_array_temp =stack[i]  # 当前直积态
        state_list_temp =[np.array(1) ] *model.get_site_number()  # 当前直积态对应的MPS直积态格式初始化

        ##  对当前直积态每个格点遍历
        for index_tuple, state_local_temp in np.ndenumerate(state_array_temp):
            assert isinstance(state_local_temp,LocalState),'参数stack内np.ndarray必须存储LocalState对象'
            mps_index =model.get_lattice().lat2mps_idx(index_tuple)
            state_list_temp[mps_index] = state_local_temp.get_amount_array()

        ##  直积态求和
        if mps is None:
            mps = MPS.from_product_state(model.get_lattice().mps_sites(), state_list_temp)
        else:
            mps = mps.add(MPS.from_product_state(model.get_lattice().mps_sites(), state_list_temp), 1, 1)

    ##  返回结果
    return mps