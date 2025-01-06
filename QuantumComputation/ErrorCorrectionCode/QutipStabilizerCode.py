import itertools
import numpy as np
from qutip import *
from QuantumComputation.ErrorCorrectionCode.StabilizerCode import StabilizerCode
from QuantumComputation.Helper.OperatorGenerator import operator_generator


class QutipStabilizerCode(StabilizerCode):
    # %% USER：构造函数
    """"
    self.N：int对象，局域个数
    """""
    def __init__(self,N):
        super().__init__(N)


    # %%  USER：计算对易式
    """
    input.g_0：list of string对象，Majorana算符字符串
    input.g_1：list of string对象，Majorana算符字符串
    output.flag：bool对象，对易则为True
    """
    def commuter(self,s_0,s_1):
        return np.isclose((s_0.dag()*s_1-s_1.dag()*s_0).norm(),0,1e-5,1e-5)


    #%%  USER：计算反对易式
    """
    input.g_0：list of string对象，Majorana算符字符串
    input.g_1：list of string对象，Majorana算符字符串
    output.flag：bool对象，反对易则为True
    """
    def anticommuter(self,s_0,s_1):
        return np.isclose((s_0.dag()*s_1+s_1.dag()*s_0).norm(),0,1e-5,1e-5)


    #%%  USER：计算稳定子空间一组基矢
    """"
    output.stable_basis_list：list of Qobj对象，稳定子空间的一组基矢
    """""
    def get_logical_space(self):
        eigenvalues,eigenvectors=self.stabilizers[0].eigenstates()  # 计算第零个稳定子的本征值和本征矢量
        stable_basis_list=eigenvectors[int(len(eigenvectors)/2)-1:-1]  # 获取所有本征值为1的本征矢量

        ##  处理第一个之后的稳定子
        for i in range(1,len(self.stabilizers)):

            ##  构造稳定子在当前子空间的矩阵表示
            matrix_temp=np.zeros((len(stable_basis_list),len(stable_basis_list)),dtype=complex)
            for j in range(len(stable_basis_list)):
                for k in range(len(stable_basis_list)):
                    matrix_temp[j][k]=stable_basis_list[j].dag()*self.stabilizers[i]*stable_basis_list[k]

            eigenvalues, eigenvectors=np.linalg.eig(matrix_temp)  # 计算当前矩阵的本征值和本征向量
            stable_basis_list_temp=[]  # 初始化当前稳定子的本征矢量列表

            ##  选取所有本征值为1的本征向量，变换到原来的本征矢的线性组合
            for l in range(len(eigenvalues)):
                if np.isclose(np.abs(eigenvalues[l]-1),0,1e-5,1e-5):
                    vector_temp=0
                    for m in range(len(stable_basis_list)):
                        vector_temp=vector_temp+stable_basis_list[m]*eigenvectors[m][l]
                    stable_basis_list_temp.append(vector_temp)

            ##  得到进一步缩小的本征子空间的本征矢量
            stable_basis_list=stable_basis_list_temp

        ##  返回结果
        return stable_basis_list


    #%%  USER：判断某个错误列表能否被纠正
    """
    input.kraus_list：list of Qobj对象，错误模型的Kraus算符列表
    output.flag：bool对象，反对易则为True
    """
    def knill_laflamme(self,kraus_list):
        ## 参数获取
        stable_basis_list = self.get_logical_space()  # 稳定子空间一组基矢

        ##  获取稳定子空间的投影算符
        P = 0
        for i in range(len(stable_basis_list)):
            P = P + stable_basis_list[i] * stable_basis_list[i].dag()

        ##  验证模块等式是否成立
        for i in range(len(kraus_list)):
            for j in range(i, len(kraus_list)):

                """
                验证下面公式成立
                $\hat P\hat E_i^\dagger\hat E_j\hat P=\alpha_{ij}\hat P$
                其中$\alpha_{ij}$是一个厄米变换
                """
                A_0 = P * kraus_list[i].dag() * kraus_list[j].dag() * P
                A_1 = P * kraus_list[j].dag() * kraus_list[i].dag() * P
                ratio_0 = A_0.full()[0, 0] / P.full()[0, 0]
                ratio_1 = A_1.full()[0, 0] / P.full()[0, 0]
                if not np.isclose((A_0 - P * ratio_0).norm(), 0, 1e-5, 1e-5):
                    return False
                if not np.isclose((A_1 - P * ratio_1).norm(), 0, 1e-5, 1e-5):
                    return False
                if not np.isclose(np.abs(ratio_0 - ratio_1.conjugate()), 0, 1e-5, 1e-5):
                    return False

        ##  如果等式都成立，则返回True
        return True


    #%%  USER：获取最大纠错权重
    """
    output.weight：int对象，该纠错码的最大纠错权重
    influence：本函数将self.weight修改为当前计算结果
    """
    def get_weight(self):
        ##  如果计算过了，就直接调取结果
        if self.weight is not None:
            return self.weight

        ##  如果没有计算过就计算
        weight=0

        ##  遍历错误权重大小，直到发现不能纠正的错误，输出它的权重减一
        for i in range(1,self.N):
            error_list=[]  # 当前权重的所有错误列表初始化

            ##  构造错误串
            pauli_ops=['X','Y','Z']  # 单个qubit上的错误类型
            params=()
            for j in range(i):
                params=params+(pauli_ops[j],)

            ##  遍历可能的错误位点
            for position_list in itertools.combinations(range(self.N), i):

                ##  遍历可能的错误串
                error = ['I'] * self.N  # 将错误初始化为单位算符
                for error_string in itertools.product(*params):

                    ##  在选取的位点子集上加入对应错误
                    for k in range(len(position_list)):
                        error[position_list[k]]=error_string[k]

                    ##  当前错误加入错误列表中
                    error_list.append(error.copy())

            ##  将错误串转化为Qobj对象
            kraus_list=[]
            for j in range(len(error_list)):
                temp=1
                for k in range(len(error_list[j])):
                    if error_list[j][k]=='X':
                        temp=temp*operator_generator(self.N,sigmax(),k)
                    elif error_list[j][k]=='Y':
                        temp=temp*operator_generator(self.N,sigmay(),k)
                    elif error_list[j][k]=='Z':
                        temp=temp*operator_generator(self.N,sigmaz(),k)
                    elif error_list[j][k]=='I':
                        temp=temp*operator_generator(self.N,identity(2),0)
                kraus_list.append(temp)

            ##  判断当前错误能否被纠正
            if not self.knill_laflamme(kraus_list):
                self.weight=weight
                return weight

            ##  如果当前权重下的错误都能纠正，则将结果加一
            weight=weight+1

