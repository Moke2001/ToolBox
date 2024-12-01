from qutip import *
import random


def measurement(psi,operator):
    assert isinstance(operator,Qobj),'operator must be Qobj'
    assert isinstance(psi,Qobj),'psi must be Qobj'

    eigenvalues,eigenstates=operator.eigenstates()
    projector_list=[]
    for i in range(len(eigenvalues)):
        projector_list.append(eigenstates[i]*eigenstates[i].dag())
    P_list=[]
    for i in range(len(projector_list)):
        P_list.append(expect(projector_list[i],psi))
    index = random.choices(range(len(P_list)), weights=P_list, k=1)[0]
    psi_result=projector_list[index]*psi
    psi_result=psi_result/psi_result.norm()

    return psi_result,eigenvalues[index]