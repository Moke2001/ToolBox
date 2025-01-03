import numpy as np
from matplotlib import pyplot as plt
from Algorithm.AlgorithmSolver.AlgorithmSolver import AlgorithmSolver
from Format.TermFormat.OverallCouplingTermFormat import OverallCouplingTermFormat
from State.StateNumpy.LocalStateNumpy import LocalStateNumpy
from State.StateNumpy.StateNumpy import StateNumpy
from Format.ModelFormat.ModelFormat import ModelFormat
from Format.SiteFormat.SiteFormat import SiteFormat
from Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Format.TermFormat.OverallOnsiteTermFormat import OverallOnsiteTermFormat


#%%  USER：定义时变函数
def zeeman(t,args):
    g_max=args.get('g_max')
    omega=args.get('omega')
    return np.sin(omega*t)*g_max


#%%  USER：主函数
def example():
    ##  SECTION：定义格点---------------------------------------------------------------------------
    site_format=SiteFormat.SpinHalfSiteFormat()

    ##  SECTION：定义晶格---------------------------------------------------------------------------
    cell_period_list=[5]
    cell_vector_list=[np.array([1])]
    inner_site_list=[site_format]
    inner_coordinate_list=[np.array([0])]

    ##  SECTION：定义模型并更新晶格-----------------------------------------------------------------
    model=ModelFormat()
    model.update_lattice(cell_period_list,cell_vector_list,inner_site_list,inner_coordinate_list)

    ##  SECTION：定义哈密顿量-----------------------------------------------------------------------
    ##  含时哈密顿量项
    function_params={
        'g_max':0.5,
        'omega':1
    }
    term = OverallOnsiteTermFormat('field', 'hamiltonian', 0, 'sigmax',zeeman,function_params)
    model.push(term)

    ##  不含时哈密顿量项
    term=OverallCouplingTermFormat('interaction','hamiltonian',0,0,(1,),'sigmaz','sigmaz',1)
    model.push(term)

    ##  SECTION：定义初态---------------------------------------------------------------------------
    x=LocalStateNumpy(2,np.array([1, 0]))
    y=LocalStateNumpy(2,np.array([0, 1]))
    state_array = np.array([[x], [x], [y], [x], [y]])
    state=StateNumpy(state_array)

    ##  SECTION：定义可观测量-----------------------------------------------------------------------
    expectation_terms = []
    for i in range(5):
        term=OnsiteTermFormat('observe','observe',(i,0),'sigmaz',1)
        expectation_terms.append(term)

    ##  SECTION：定义模拟---------------------------------------------------------------------------
    t_list=np.linspace(0,1,20)
    psi_result,data_list=AlgorithmSolver.EvolutionSolver(model,state,expectation_terms,t_list,'tenpy')

    ##  SECTION：输出结果---------------------------------------------------------------------------
    plt.plot(t_list,data_list[1])
    plt.show()


if __name__=="__main__":
    example()
