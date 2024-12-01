
import random
import numpy as np
from tenpy import MPS
from TenpyToolBox.Package.ModelPackage import ModelPackage


def measurement(psi,projector_list,value_list,position,model:ModelPackage):
    mps_index=model.get_mps_index(position)
    assert isinstance(psi,MPS),'psi must be an MPS object'
    psi_result=psi.copy()
    probability_list=[]
    for i in range(len(projector_list)):
        probability_list.append(psi_result.expectation_value(projector_list[i],mps_index))
    assert np.abs(sum(probability_list)-1)<0.00001,'probability list must sum to 1'
    result_state = random.choices(range(len(probability_list)), weights=probability_list, k=1)[0]
    psi_result.apply_local_op(mps_index,projector_list[result_state])
    return psi_result,value_list[result_state]