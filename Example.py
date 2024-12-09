import numpy as np
from matplotlib import pyplot as plt

from Format.AlgorithmFormat.EvolutionSolverFormat import EvolutionSolverFormat
from Format.LatticeFormat.LatticeFormat import LatticeFormat
from Format.ModelFormat.ModelFormat import ModelFormat
from Format.SiteFormat.SpinHalfSiteFormat import SpinHalfSiteFormat
from Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Format.TermFormat.OverallOnsiteTermFormat import OverallOnsiteTermFormat
from QutipBox.AlgorithmQutip.EvolutionSolverQutip import EvolutionSolverQutip
from QutipBox.ModelQutip.ModelQutip import ModelQutip
from QutipBox.StateQutip.StateQutip import StateQutip
from TenpyBox.AlgorithmTenpy.EvolutionSolverTenpy import EvolutionSolverTenpy
from TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy
from TenpyBox.StateTenpy.StateTenpy import StateTenpy


def zeeman(t,args):
    g_max=args.get('g_max')
    omega=args.get('omega')
    return np.sin(omega*t)*g_max

def example():
    site_format=SpinHalfSiteFormat(None)
    cell_period_list=[5]
    cell_vector_list=[np.array([1])]
    inner_site_list=[site_format]
    inner_coordinate_list=[np.array([0])]

    model_format=ModelFormat()
    model_format.update_lattice(cell_period_list,cell_vector_list,inner_site_list,inner_coordinate_list)

    function_params={
        'g_max':0.5,
        'omega':1
    }
    term = OverallOnsiteTermFormat('field', 'hamiltonian', 0, 'sigmax',zeeman,function_params)
    model_format.push(term)
    for i in range(5-1):
        term=CouplingTermFormat('interaction','hamiltonian',(i,0),(i+1,0),'sigmaz','sigmaz',1)
        model_format.push(term)


    model=ModelTenpy(model_format)
    state_array=np.array([[1],[0],[1],[1],[1]])
    psi=StateTenpy.get_product_state(model,state_array)
    expectation_terms = []
    for i in range(5):
        term=OnsiteTermFormat('observe','observe',(i,0),'sigmaz',1)
        expectation_terms.append(term)
    t_list=np.linspace(0,1,5)
    engine=EvolutionSolverTenpy(model,psi,expectation_terms,t_list)
    engine.compute(10,20)
    data_list,psi_final=engine.get_result()
    plt.plot(t_list,data_list[1])
    plt.show()


if __name__=="__main__":
    example()
