import numpy as np
from matplotlib import pyplot as plt
from Algorithm.AlgorithmSolver.AlgorithmSolver import AlgorithmSolver
from Data.LocalState.LocalState import LocalState
from Data.State.State import State
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.SiteFormat.SpinHalfSiteFormat import SpinHalfSiteFormat
from Framework.Format.TermFormat.CouplingTermFormat import CouplingTermFormat
from Framework.Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Framework.Format.TermFormat.OverallOnsiteTermFormat import OverallOnsiteTermFormat
from Framework.TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy


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

    x=LocalState(2,np.array([1,0]))
    y=LocalState(2,np.array([0,1]))
    model=ModelTenpy(model_format)
    state_array = [np.array([[x], [x], [y], [x], [y]])]
    psi=State()
    psi.initial(state_array)
    expectation_terms = []
    for i in range(5):
        term=OnsiteTermFormat('observe','observe',(i,0),'sigmaz',1)
        expectation_terms.append(term)
    t_list=np.linspace(0,1,5)
    psi_result,data_list=AlgorithmSolver.EvolutionSolver(model,psi,expectation_terms,t_list,'qutip')
    plt.plot(t_list,data_list[1])
    plt.show()


if __name__=="__main__":
    example()
