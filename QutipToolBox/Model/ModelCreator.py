##---Create specific model in Qutip---##
from QutipToolBox.Lattice.LatticeCreator import lattice_creator
from QutipToolBox.Site.Site import Site
from qutip import *
from QutipToolBox.Model.Model import Model


def model_creator(model_parameter):
    name=model_parameter.gets('name', None)
    lattice_parameter=model_parameter.gets('lattice_parameter', None)
    lattice=lattice_creator(lattice_parameter)

    ##  横场Ising模型
    if name is 'TFIM':
        operator_list=[]
        interaction_length=model_parameter.gets('interaction_length', 1.0)
        J=model_parameter.gets('J', 1.0)
        g=model_parameter.gets('g', 1.0)
        for i in range(lattice.get_site_number()):
            operator_list.append((i,g*sigmax()))
            for j in range(i+1,lattice.get_site_number()):
                if Site.distance(lattice.get_site[i],lattice.get_site[j])<interaction_length:
                    operator_list.append((i,J*sigmaz(),j,sigmaz()))

    ##  Heisenberg模型
    elif name is 'Heisenberg':
        operator_list=[]
        interaction_length=model_parameter.gets('interaction_length', 1.0)
        for i in range(lattice.get_site_number()):
            for j in range(i+1,lattice.get_site_number()):
                if Site.distance(lattice.get_site[i],lattice.get_site[j])<interaction_length:
                    operator_list.append((i,sigmax(),j,sigmax()))
                    operator_list.append((i, sigmay(), j, sigmay()))
                    operator_list.append((i, sigmaz(), j, sigmaz()))

    ##  抛出类型错误
    else:
        raise ValueError('There is no such type of model')

    ##  返回结果
    return Model(lattice,operator_list)
