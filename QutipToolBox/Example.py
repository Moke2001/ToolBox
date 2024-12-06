import numpy as np
from matplotlib import pyplot as plt

from Framework.Term.CouplingTerm import CouplingTerm
from Framework.Term.OverallOnsiteTerm import OverallOnsiteTerm
from QutipToolBox.Dynamics.UnitaryEvolve import unitary_evolve
from QutipToolBox.Lattice.Lattice import Lattice
from QutipToolBox.Model.Model import Model
from QutipToolBox.Site.SpinHalfSite import SpinHalfSite


def function(t,function_params):
    g_max=function_params.get('g_max')
    omega=function_params.get('omega')
    return g_max*np.sin(t*omega)


def example():
    ##  构造晶格
    Ls=[3,2]
    unit_vectors=[np.array([1,0]),np.array([0,1])]
    cell_sites=[SpinHalfSite()]
    cell_vectors=[np.array([0,0])]
    lattice=Lattice(Ls, unit_vectors, cell_sites, cell_vectors)

    ##  构造模型
    model=Model()
    model.lattice_build(lattice)

    ##  构造哈密顿量
    model.push(OverallOnsiteTerm('field','hamiltonian',0,'sigmax',function,{'g_max':1,'omega':0.5}))
    for i_0 in range(3):
        for j_0 in range(2):
            for i_1 in range(3):
                for j_1 in range(2):
                    if model.get_distance((i_0,j_0,0),(i_1,j_1,0))<=1.01:
                        model.push(CouplingTerm('interaction','hamiltonian',(i_0,j_0,0),(i_1,j_1,0),'sigmaz','sigmaz',1))

    state_tensor=np.array([[[0],[0]],[[1],[1]],[[0],[0]]],dtype=int)
    psi=model.get_product_state(state_tensor)
    t_list=np.linspace(0,1,9)
    result,psi=unitary_evolve(model, psi, t_list, [model.get_operator('sigmaz',(1,1,0))])
    plt.plot(t_list,result[0])
    plt.show()

if __name__=='__main__':
    example()