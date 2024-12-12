from qutip import Qobj
from Data.StateVectorTools.Term2Qobj import term2qobj
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.TermFormat.TermFormat import TermFormat
from Framework.Format.TermFormat.TermsFormat import TermsFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
term2qobj：计算作用量的qutip形式算符
input.model_origin：ModelFormat对象，算符所在的模型
input.vector_origin：Qobj对象，qutip形式态矢量
input.term：TermsFormat对象或TermFormat对象
normalize：bool对象，判断是否归一化
output.vector：Qobj对象，结果态矢
influence：本函数不改变参数对象
"""
def vector_apply(model_origin,vector_origin,term,normalize):
    #%%  BLOCK：标准化
    assert isinstance(term, TermFormat) or isinstance(term, TermsFormat), '参数term必须是TermFormat或TermsFormat对象'
    assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
    assert isinstance(vector_origin,Qobj),'参数vector_origin必须是Qobj对象'
    assert isinstance(normalize,bool),'参数normalize必须是bool对象'


    #%%  BLOCK：计算结果
    model=model_preparer(model_origin,'qutip')
    op = term2qobj(model,term)
    vector = op * vector_origin


    #%%  BLOCK：返回结果
    if normalize:
        return vector / vector.norm()
    else:
        return vector
