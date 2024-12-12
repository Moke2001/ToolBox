import numpy as np
from tenpy import MPS
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Framework.Format.TermFormat.MultiTermFormat import MultiTermFormat
from Framework.Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Framework.Format.TermFormat.TermFormat import TermFormat
from Framework.Format.TermFormat.TermsFormat import TermsFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
mps_expectation：计算态矢在可观测量下的期望
input.model_origin：ModelFormat对象，MPS所在的模型
input.mps：MPS对象，态矢
input.term：TermFormat对象，可观测量算符
output.value：float对象
influence：本函数不改变参数对象
"""
def mps_expectation(model_origin:ModelFormat, mps:MPS,term:TermFormat or TermsFormat):
    ##  标准化环节
    assert isinstance(model_origin, ModelFormat),'参数model_origin必须是ModelFormat对象'
    assert isinstance(mps,MPS),'参数mps必须是MPS对象'
    assert isinstance(term,TermsFormat) or isinstance(term,TermFormat),'参数term必须是TermsFormat或TermFormat对象'
    model=model_preparer(model_origin,'qutip')
    value = 0

    ##  如果是单一作用量，直接计算
    if isinstance(term, TermFormat):
        assert term.time==False,'参数term不允许含时'

        ##  计算OnsiteTermFormat可观测量的期望
        if isinstance(term, OnsiteTermFormat):
            op = term.get_op()
            index_tuple = term.get_position()
            mps_index = model.get_mps_index_tenpy(index_tuple)
            value=mps.expectation_value(op, [mps_index])

        ##  计算CouplingTermFormat可观测量的期望
        elif isinstance(term, CouplingTermFormat):
            op_0, op_1 = term.get_op()
            index_tuple_0, index_tuple_1 = term.get_position()
            mps_index_0 = model.get_mps_index_tenpy(index_tuple_0)
            mps_index_1 = model.get_mps_index_tenpy(index_tuple_1)
            value=mps.expectation_value_term([(op_0,mps_index_0),(op_1,mps_index_1)])

        ##  计算MultiTermFormat可观测量的期望
        elif isinstance(term, MultiTermFormat):
            op_list = term.get_op()
            index_tuple_list = term.get_position()
            mps_index_list = []
            for i in range(len(index_tuple_list)):
                mps_index_list.append(model.get_mps_index_tenpy(index_tuple_list[i]))
            parameter_list=[]
            for i in range(len(mps_index_list)):
                parameter_list.append((op_list[i],mps_index_list[i]))
            value=mps.expectation_value_term(parameter_list)

        ##  计算Overall可观测量的期望，用MPO成员函数
        else:
            model_format_temp=ModelFormat()
            model_format_temp.insert_lattice(model)
            model_format_temp.push(term)
            model_temp=model_preparer(model_format_temp,'tenpy')
            H=model_temp.get_model().calc_H_MPO()
            value=H.expectation_value(mps)

    ##  如果是TermsFormat对象，递归计算求和
    elif isinstance(term, TermsFormat):
        for i in range(term.number):
            value=mps_expectation(model,mps,term.get_term(i))+value

    ##  已经限定类型，不用重复报错
    else:
        pass

    ##  返回期望值，忽略计算中的虚数部分
    return np.real(value)


"""
mps_apply：计算算符作用后的态矢
input.model_origin：ModelFormat对象，MPS所在的模型
input.mps_origin：MPS对象，初始态矢
input.term：TermFormat对象，可观测量算符
input.normalize：bool对象，决定结果是否重新归一化
output.mps：MPS对象，作用算符后的态矢
influence：本函数不改变参数对象
"""
def mps_apply(model_origin, mps_origin, term, normalize):
    ##  标准化环节
    assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
    assert isinstance(mps_origin, MPS), '参数mps_origin必须是MPS对象'
    assert isinstance(term, TermsFormat) or isinstance(term, TermFormat), '参数term必须是TermsFormat或TermFormat对象'
    assert isinstance(normalize,bool),'参数normalize必须是bool对象'
    model=model_preparer(model_origin,'tenpy')
    mps=mps_origin.copy()

    ##  如果是单一作用量，直接计算
    if isinstance(term, TermFormat):

        ##  计算OnsiteTermFormat算符作用后的结果
        if isinstance(term, OnsiteTermFormat):
            index_tuple = term.get_position()
            op = term.get_op()
            mps_index = model.get_mps_index_tenpy(index_tuple)
            mps.apply_local_op(mps_index, op, renormalize=normalize)

        ##  计算CouplingTermFormat算符作用后的结果
        elif isinstance(term, CouplingTermFormat):
            index_tuple_0, index_tuple_1 = term.get_position()
            op_0, op_1 = term.get_op()
            mps_index_0 = model.get_mps_index_tenpy(index_tuple_0)
            mps_index_1 = model.get_mps_index_tenpy(index_tuple_1)
            mps.apply_local_op(mps_index_0, op_0, renormalize=normalize)
            mps.apply_local_op(mps_index_1, op_1, renormalize=normalize)

        ##  计算MultiTermFormat算符作用后的结果
        elif isinstance(term, MultiTermFormat):
            index_tuple_list = term.get_position()
            op_list = term.get_op()
            mps_index_list = []
            for i in range(len(index_tuple_list)):
                mps_index_list.append(model.get_mps_index_tenpy(index_tuple_list[i]))
            for i in range(len(mps_index_list)):
                mps.apply_local_op(mps_index_list[i], op_list[i], renormalize=normalize)

        ##  计算Overall算符作用后的结果
        else:
            model_format_temp = ModelFormat()
            model_format_temp.insert_lattice(model)
            model_format_temp.push(term)
            model_temp = model_preparer(model_format_temp, 'tenpy')
            H = model_temp.get_model().calc_H_MPO()
            mps = H.apply(mps)
            mps.canonical_form()

    ##  如果是TermsFormat对象，递归应用算符
    elif isinstance(term, TermsFormat):
        for i in range(term.number):
            mps=mps_apply(model_origin, mps, term, normalize)

    ##  已经限定类型，不用重复报错
    else:
        pass

    ##  返回作用后的结果
    return mps


"""
mps_overlap：计算两个态矢的投影
input.mps_0：MPS对象，左矢
input.mps_1：MPS对象，右矢
output：complex对象，投影值
influence：本函数不改变参数对象
"""
def mps_overlap(mps_0,mps_1):
    assert isinstance(mps_0,MPS) and isinstance(mps_1,MPS)
    return mps_1.overlap(mps_0)
