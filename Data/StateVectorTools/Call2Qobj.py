import numpy as np
from qutip import Qobj, tensor
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
call2qobj：将特定位置上的局域算符转换为全局qutip形式算符
input.model_origin：ModelFormat对象，算符所在的模型
input.name：str对象，局域算符名称
index_tuple：tuple对象，算符位置
"""
def call2qobj(model_origin,name,index_tuple)->Qobj:
    ##  标准化
    assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
    assert isinstance(name,str),'参数name必须是str对象'
    assert isinstance(index_tuple,tuple),'参数index_tuple必须是tuple对象'
    model = model_preparer(model_origin, 'qutip')

    ##  计算单一算符全局形式
    result = None  # 结果初始化
    for op_index_tuple, op_iteration in np.ndenumerate(model.get_lattice()):

        ##  头一个结果直接赋值
        if result==None:
            if op_index_tuple==index_tuple:
                result=model.get_site(index_tuple).get_local_operator_qutip(name)
            else:
                result=model.get_site(op_index_tuple).get_local_operator_qutip('identity')

        ##  后面的做张量积
        else:
            if op_index_tuple==index_tuple:
                result=tensor(result,model.get_site(index_tuple).get_local_operator_qutip(name))
            else:
                result=tensor(result,model.get_site(op_index_tuple).get_local_operator_qutip('identity'))

    ##  返回结果
    return result