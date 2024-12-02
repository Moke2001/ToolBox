##  矩阵包：用名称生成所需要的矩阵的array形式
import numpy as np


class MatrixPackage():
    ##  构造函数
    def __init__(self):
        pass


    @classmethod
    ##  由名称生成矩阵的array形式
    def get_array(cls,type):
        if type=='sigmax':
            matrix=np.array([[0,1],[1,0]],dtype=complex)
        elif type=='sigmay':
            matrix=np.array([[0,-1j],[1j,0]],dtype=complex)
        elif type=='sigmaz':
            matrix=np.array([[1,0],[0,-1]],dtype=complex)
        elif type=='sigmaup':
            matrix=np.array([[1,0],[0,0]],dtype=complex)
        elif type=='sigmadown':
            matrix=np.array([[0,0],[0,1]],dtype=complex)
        elif type=='sigmaplus':
            matrix=np.array([[0,1],[0,0]],dtype=complex)
        elif type=='sigmaminus':
            matrix=np.array([[0,0],[1,0]],dtype=complex)
        elif type=='identity':
            matrix=np.array([[1,0],[0,1]],dtype=complex)
        else:
            raise ValueError("Type does not exist")
        return matrix

    ##  SpinHalfSite所需要的矩阵名称列表
    spin_half_site=['sigmax','sigmay','sigmaz','sigmaup','sigmadown','sigmaplus','sigmaminus','identity']