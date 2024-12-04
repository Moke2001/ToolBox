import random
import numpy as np
from tenpy import MPS
from TenpyToolBox.Package.ModelPackage.ModelPackage import ModelPackage


#%%  BLOCK：测量下随机坍缩
"""
输入量：态矢，投影算符列表，本征值列表，测量位置，模型
输出量：坍缩态矢，测量结果
对一个MPS对象做投影算符决定的测量，要求投影算符求和是归一化的
对应可观测量是投影算符与本征值相乘求和的结果
只针对局域测量操作
"""
def measurement(psi:MPS,projector_list:list,value_list:list,position:tuple,model:ModelPackage):
    ##  获取信息
    mps_index=model.mps_index2position(position)  # 获取测量位点的mps_index
    psi_result=psi.copy()  # 不改变原态矢
    
    ##  计算本征值投影几率
    probability_list=[]
    for i in range(len(projector_list)):
        probability_list.append(psi_result.expectation_value(projector_list[i],mps_index))
    assert np.abs(sum(probability_list)-1)<0.00001,'probability list must sum to 1'  # 要求几率归一化
    
    ##  随机坍缩到一个本征态
    result_state = random.choices(range(len(probability_list)), weights=probability_list, k=1)[0]
    psi_result.apply_local_op(mps_index,projector_list[result_state])
    
    ##  返回结果
    return psi_result,value_list[result_state]