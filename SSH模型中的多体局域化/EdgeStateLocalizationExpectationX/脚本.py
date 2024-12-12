import numpy as np
from matplotlib import pyplot as plt
from Algorithm.AlgorithmSolver.AlgorithmSolver import AlgorithmSolver
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.SiteFormat.SpinHalfSiteFormat import SpinHalfSiteFormat
from Framework.Format.TermFormat.OnsiteTermFormat import OnsiteTermFormat
from Framework.Format.TermFormat.OverallCouplingTermFormat import OverallCouplingTermFormat


def main(N,J_1,J_2,J_z,g_z,disorder,t_list,psi,disorder_type,expectation_type):
    ##  构造系统晶格
    site_format = SpinHalfSiteFormat(None)  # 格点类型
    cell_period_list = [N]  # 元胞延展次数
    cell_vector_list = [np.array([1])]  # 元胞位移
    inner_site_list = [site_format,site_format]  # 元胞内格点组
    inner_coordinate_list = [np.array([0]),np.array([0.5])]  # 元胞内格点位置
    model = ModelFormat()
    model.update_lattice(cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)

    ##  元胞间的相互作用
    term = OverallCouplingTermFormat('J1x', 'hamiltonian', 1,0,[1],'sigmax','sigmax',J_2)
    model.push(term)
    term = OverallCouplingTermFormat('J1y', 'hamiltonian', 1, 0, [1], 'sigmay', 'sigmay', J_2)
    model.push(term)

    ##  元胞内的相互作用
    term = OverallCouplingTermFormat('J2x', 'hamiltonian', 0, 1, [0], 'sigmax', 'sigmax', J_1)
    model.push(term)
    term = OverallCouplingTermFormat('J2y', 'hamiltonian', 0, 1, [0], 'sigmay', 'sigmay', J_1)
    model.push(term)


    ## 横贯相互作用
    term = OverallCouplingTermFormat('J1z', 'hamiltonian', 0, 1, [0], 'sigmaz', 'sigmaz', J_z)
    model.push(term)
    term = OverallCouplingTermFormat('J2z', 'hamiltonian', 1, 0, [1], 'sigmaz', 'sigmaz', J_z)
    model.push(term)

    ##  无序项
    if isinstance(disorder_type,list):
        for i in range(N):
            for j in range(2):
                s = np.random.uniform(g_z - disorder, g_z + disorder, 1)[0]
                for k in range(len(disorder_type)):
                    term=OnsiteTermFormat('disorder','hamiltonian',(i,j),disorder_type[k],s)
                    model.push(term)
    else:
        for i in range(N):
            for j in range(2):
                s = np.random.uniform(g_z - disorder, g_z + disorder, 1)[0]
                term = OnsiteTermFormat('disorder', 'hamiltonian', (i, j),disorder_type, s)
                model.push(term)


    ##  构造可观测量
    M_start = OnsiteTermFormat('obserbe', 'observe', (0, 0), expectation_type, 1)
    M_end=OnsiteTermFormat('obserbe', 'observe', (N-1, 1), expectation_type, 1)
    M_mid=OnsiteTermFormat('obserbe', 'observe', (int(N/2), 1), expectation_type, 1)

    ##  演化
    psi,data_list=AlgorithmSolver.EvolutionSolver(model,psi,[M_start,M_end,M_mid],t_list,'qutip')

    ##  绘图
    for i in range(len(data_list)):
        plt.plot(t_list,data_list[i])
    plt.legend(['sigma-start','sigma-end','sigma-mid'])
    plt.grid()