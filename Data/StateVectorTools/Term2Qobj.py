import numpy as np
from qutip import Qobj
from Data.StateVectorTools.Call2Qobj import call2qobj
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Framework.Format.TermFormat.MultiTermFormat import MultiTermFormat
from Framework.Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Framework.Format.TermFormat.OverallCouplingTermFormat import OverallCouplingTermFormat
from Framework.Format.TermFormat.OverallMultiTermFormat import OverallMultiTermFormat
from Framework.Format.TermFormat.OverallOnsiteTermFormat import OverallOnsiteTermFormat
from Framework.Format.TermFormat.TermFormat import TermFormat
from Framework.Format.TermFormat.TermsFormat import TermsFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


"""
term2qobj：计算作用量的qutip形式算符
input.model_origin：ModelFormat对象，算符所在的模型
input.term：TermsFormat对象或TermFormat对象
"""
def term2qobj(model_origin,term)->Qobj:
    #%%  BLOCK：标准化
    assert isinstance(term,TermFormat) or isinstance(term,TermsFormat),'参数term必须是TermFormat或TermsFormat对象'
    assert isinstance(model_origin,ModelFormat),'参数model_origin必须是ModelFormat对象'
    model=model_preparer(model_origin,'qutip')


    #%%  BLOCK：单一算符直接给出结果
    qobj=0
    if isinstance(term,TermFormat):
        assert term.time==False,'参数term必须不含时'


        #%%  SECTION：OnsiteTermFormat作用量
        if isinstance(term,OnsiteTermFormat):
            qobj=call2qobj(model,term.get_op(),term.get_position())*term.get_strength()


        #%%  SECTION：CouplingTermFormat作用量
        elif isinstance(term,CouplingTermFormat):
            op_0,op_1=term.get_op()  # 两个算符名称
            index_tuple_0,index_tuple_1=term.get_position()  # 两个位点
            qobj=call2qobj(model,op_0,index_tuple_0)*call2qobj(model,op_1,index_tuple_1)*term.get_strength()


        #%%  SECTION：MultiTermFormat作用量
        elif isinstance(term,MultiTermFormat):
            op_list=term.get_op()  # 算符名称列表
            index_tuple_list=term.get_position()  # 位点列表
            qobj=1  # 结果初始化
            for i in range(len(op_list)):
                qobj=qobj*call2qobj(model,op_list[i],index_tuple_list[i])


        #%%  SECTION：OverallOnsiteTermFormat作用量
        elif isinstance(term,OverallOnsiteTermFormat):
            op=term.get_op()  # 算符名称
            inner_index=term.get_position()  # 胞内序号

            ##  对晶格遍历
            for index_tuple, site_iteration in np.ndenumerate(model.get_lattice()):

                ##  发现胞内坐标符合的就停下来求和
                if index_tuple[-1]==inner_index:
                    qobj=qobj+call2qobj(model,op,index_tuple)

            ##  加上强度
            qobj=qobj*term.get_strength()


        #%%  SECTION：OverallCouplingTermFormat作用量
        elif isinstance(term,OverallCouplingTermFormat):
            op_0,op_1 = term.get_op()  # 算符名称
            inner_index_0,inner_index_1,cell_vector = term.get_position()  # 胞内序号和相对格位移

            ##  遍历晶格
            for index_tuple_iteration, site_iteration in np.ndenumerate(model.get_lattice()[...,0]):
                index_tuple_0_temp=index_tuple_iteration+(inner_index_0,)  # 第一个作用位点
                index_tuple_1_temp=()  # 第二个作用位点初始化
                for i in range(len(cell_vector)):
                    index_tuple_1_temp=index_tuple_1_temp+(cell_vector[i],)
                index_tuple_1_temp=index_tuple_1_temp+(inner_index_1,)

                ##  判断位点不要跳出晶格范围
                if all(index_tuple_1_temp[it]<model.cell_period_list[it] for it in range(len(model.cell_period_list))):
                    qobj = qobj + call2qobj(model, op_0, index_tuple_0_temp)*call2qobj(model, op_1, index_tuple_1_temp)

            ##  加上强度
            qobj=qobj*term.get_strength()


        #%%  SECTION：OverallMultiTermFormat作用量
        elif isinstance(term,OverallMultiTermFormat):
            op_list=term.get_op()  # 算符名称
            inner_index_list,cell_vector_list=term.get_unit()  # 胞内序号和相对格位移

            ##  遍历晶格
            for index_tuple_iteration, site_iteration in np.ndenumerate(model.get_lattice()[...,0]):
                index_tuple_list_temp=[]
                flag=True
                for i in range(len(inner_index_list)):
                    index_tuple_temp=()
                    for j in range(len(index_tuple_iteration)):
                        index_tuple_temp=index_tuple_temp+(index_tuple_list_temp[j]+cell_vector_list[j],)
                    index_tuple_temp=index_tuple_temp+(inner_index_list[i],)
                    index_tuple_list_temp.append(index_tuple_temp)

                ##  添加判断格点是否跳出范围
                for i in range(len(index_tuple_list_temp)):
                    if not all(index_tuple_list_temp[i][it] < model.cell_period_list[it] for it in range(len(index_tuple_list_temp[i]))):
                        flag=False
                        break

                ##  格点在晶格内时计算算符乘积
                if flag:
                    for i in range(len(op_list)):
                        if i==0:
                            qobj=call2qobj(model, op_list[i], index_tuple_list_temp[i])
                        else:
                            qobj=qobj*call2qobj(model, op_list[i], index_tuple_list_temp[i])

            ##  加上强度
            qobj=qobj*term.get_strength()


    #%%  BLOCK：作用量列表递归调用
    elif isinstance(term,TermsFormat):
        for i in range(term.number):
            qobj=qobj+term2qobj(model,term.get_term(i))


    #%%  BLOCK：不考虑其他情况
    else:
        pass


    #%%  BLOCK：返回结果
    return qobj