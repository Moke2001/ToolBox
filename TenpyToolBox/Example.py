import numpy as np
from tenpy import SpinHalfSite, Lattice
from TenpyToolBox.Dynamics.EvolveTDVP import evolve_tdvp
from TenpyToolBox.Dynamics.Measurement import measurement
from TenpyToolBox.LinearPackage.MatrixPackage import MatrixPackage
from TenpyToolBox.ModelPackage.ModelPackage import ModelPackage
from Framework.Term.OnsiteTerm import OnsiteTerm
from Framework.Term.OverallCouplingTerm import OverallCouplingTerm


def example():
    ##  TODO：构造site对象----------------------------------------------------------------
    site = SpinHalfSite(conserve=None)
    for op_name in MatrixPackage.spin_half_site:
        site.add_op(op_name,MatrixPackage.get_array(op_name))

    ##  TODO：构造lattice对象----------------------------------------------------------------
    L_x=3
    L_y=3
    Ls=[L_x,L_y]
    unit_cell=[site]
    bc='open'
    bc_MPS='finite'
    basis=np.array([[1,0],[0,1]])
    positions=np.array([[0,0],])
    lattice=Lattice(Ls, unit_cell, bc=bc, bc_MPS=bc_MPS, basis=basis, positions=positions)

    ##  TODO：构造model对象----------------------------------------------------------------
    model=ModelPackage()
    model.update_lattice(lattice)
    T=5
    g_A_max=1
    g_A_min=0
    function_params={
        'T':T,
        'g_A_max':g_A_max,
        'g_A_min':g_A_min,
    }
    for i in range(L_x):
        for j in range(L_y):
            term=OnsiteTerm('transverse field','hamiltonian',(i,j,0),'sigmax',function,function_params)
            model.push(term)
    strength=1
    term=OverallCouplingTerm('interaction','hamiltonian',0,0,[1,0],'sigmaz','sigmaz',strength)
    model.push(term)

    ##  TODO: 演化-------------------------------------------------------------------------------
    psi = model.state_creator('random',10)  # 态矢初始化
    psi=evolve_tdvp(T/40,40,40,psi,model)
    psi,value=measurement(psi,['sigmaup','sigmadown'],[1,0],(1,1,0),model)
    print(value)


##  TODO：含时系统时变函数----------------------------------------------------------------------------
def function(time, function_params):
    ##  参数获取
    T = function_params.get('T', 1)  # 扫描总时间
    g_A_max = function_params.get('g_A_max', 0.1)  # 最大场强
    g_A_min = function_params.get('g_A_min', 0)  # 最小场强
    factor=function_params.get('factor', -1)
    k_g_A = (g_A_max - g_A_min) / (3 * T / 4)  # 场强变化率

    ##  前3/4时间均匀减小场强
    if time < 3 * T / 4:
        return factor*(g_A_max - k_g_A * time)

    ##  后1/4时间保持场强
    elif 3 * T / 4 <= time <= T:
        return factor*g_A_min
    else:
        raise ValueError('Time is out of range')


if __name__=='__main__':
    example()