import copy
import itertools
import galois
import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.CliffordSimulator.MajoranaComputer import MajoranaComputer
from Physics.QuantumComputation.StabilizerSimulator.Group.MajoranaGroup import MajoranaGroup


class MajoranaCode:
    # %%  USER：空构造函数
    """""
    self.N：int对象，稳定子数目
    self.stabilizers：list of PauliOperator对象，稳定子生成元
    self.weight：int对象，编码最大能纠正的Pauli error的权重
    """""
    def __init__(self, majorana_computer, generator_vector):
        self.computer = majorana_computer
        self.N=self.computer.N
        self.generator_vector = np.array(generator_vector, dtype=MajoranaGroup)
        self.weight = None


    # %%  USER：计算能纠正的最大错误
    def get_weight(self):
        ##  如果计算过了，就直接调取结果
        if self.weight is not None:
            return self.weight

        ##  如果没有计算过就计算
        weight = 0

        ##  遍历错误权重大小，直到发现不能纠正的错误，输出它的权重减一
        syndrome_list = []
        error_list = []
        for i in range(1, self.N):
            """
            选取所有可能的错误位
            例如如果有3个qubits，权重为2，那么为：[(0,1),(0，2),(1,2)]
            """
            error_position_list = itertools.combinations(range(self.N*2), i)
            for error_position in error_position_list:
                error_list.append(MajoranaGroup(self.N,1,error_position))

            """
            用KL定理分析当前权重的所有错误能否被纠正
            首先计算当前错误列表的征状列表，如果它错误征状唯一则可以被纠正
            如果不唯一，则判断是否简并
            """
            flag = len(syndrome_list)  # 当前征状列表长度
            for j in range(flag, len(error_list)):
                syndrome_temp = []
                for k in range(len(self.generator_vector)):
                    g_temp = self.generator_vector[k]
                    assert isinstance(g_temp, MajoranaGroup)
                    if g_temp.commuter(error_list[j]):
                        syndrome_temp.append(0)
                    else:
                        syndrome_temp.append(1)
                syndrome_list.append(syndrome_temp)

            ##  查找征状相同的错误
            for j in range(flag, len(syndrome_list)):

                ##  如果全为0，要判断在不在稳定子内
                if all(x == 0 for x in syndrome_list):
                    if self.independent_checker(error_list[j]):
                        self.weight = weight
                        return weight
                for k in range(j):

                    ##  如果征状相同，计算是否简并
                    if syndrome_list[j] == syndrome_list[k]:
                        temp = error_list[k] * error_list[j]
                        if self.independent_checker(temp):
                            self.weight = weight
                            return weight

            ##  如果当前权重下的错误都能纠正，则将结果加一
            weight = weight + 1


    # %%  USER：复制函数
    """
    output：PauliStabilizer对象，本对象的复制
    """
    def copy(self):
        return copy.deepcopy(self)


    # %%  USER：判断是否独立
    """
    output：bool对象，独立为True，不独立为False
    """
    def independent_checker(self, *args):
        ##  没有参数，判断当前稳定子生成元是否独立
        if len(args) == 0:

            ##  计算校验矩阵
            check_matrix = np.zeros((self.generator_vector.shape[0], self.N * 2), dtype=int)
            for i in range(self.generator_vector.shape[0]):
                for j in range(self.N * 2):
                    check_matrix[i, j] = self.generator_vector[i][j]

            ##  计算校验矩阵的01域上的形式
            GF = galois.GF(2 ** 1)
            check_matrix = GF(check_matrix)

            ##  根据矩阵01秩计算是否独立
            if np.linalg.matrix_rank(check_matrix) == check_matrix.shape[0]:
                return True
            else:
                return False

        ##  如果有参数，则需要判断新算符是否与其他稳定子独立
        elif len(args) == 1:
            assert isinstance(args[0], MajoranaGroup)

            ##  计算校验矩阵
            check_matrix = np.zeros((self.generator_vector.shape[0] + 1, self.N * 2), dtype=int)
            for i in range(self.generator_vector.shape[0]):
                for j in range(self.N * 2):
                    check_matrix[i, j] = self.generator_vector[i][j]
            for i in range(self.N * 2):
                check_matrix[-1, i] = args[0][i]

            ##  计算校验矩阵的01域上的形式
            GF = galois.GF(2 ** 1)
            check_matrix = GF(check_matrix)

            ##  根据矩阵01秩计算是否独立
            if np.linalg.matrix_rank(check_matrix) == check_matrix.shape[0]:
                return True
            else:
                return False

        ##  其他参数数目抛出错误
        else:
            raise ValueError("Incorrect number of arguments")


    # %%  USER：计算编码率
    def get_ratio(self):
        return (self.N - len(self.generator_vector)) / self.N


    #%%  USER：获取逻辑算符
    def get_logical_operator(self):
        ##  构造校验矩阵
        check_matrix=np.zeros((self.N * 2, self.N * 2), dtype=int)
        for i in range(self.generator_vector.shape[0]):
            for j in range(self.N * 2):
                check_matrix[i, j] = self.generator_vector[i][j]
        GF = galois.GF(2)
        check_matrix = GF(check_matrix)

        # 计算原始零空间基矢
        null_space = check_matrix.null_space()
        zeros_vector=GF(np.zeros(self.N*2,dtype=int))
        # 筛选与行空间无关的基矢
        independent_null_basis_list=[]
        for vec in null_space:
            number=len(independent_null_basis_list)
            check_matrix[number+self.generator_vector.shape[0]+1,:]=GF(np.array(vec,dtype=int))
            if np.linalg.matrix_rank(check_matrix)==number+self.generator_vector.shape[0]+1:
                independent_null_basis_list.append(vec)
            else:
                check_matrix[number+self.generator_vector.shape[0]+1,:]=zeros_vector

        # 正交化过程
        ortho_basis = []
        for vec in independent_null_basis_list:
            # 复制向量以避免修改原始数据
            v = vec.copy()

            # 对现有正交基矢进行正交化
            for u in ortho_basis:
                dot_product = np.dot(v, u)
                if dot_product:
                    v += u  # GF(2)中的加法等价于异或

            ortho_basis.append(v)

        return ortho_basis


if __name__ == '__main__':
    majorana_computer=MajoranaComputer(7,0.01)
    s_0 = MajoranaGroup(7, 1j, [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    s_1 = MajoranaGroup(7, 1j, [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0])
    s_2 = MajoranaGroup(7, 1j, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0])
    s_3 = MajoranaGroup(7, 1j, [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1])
    s_4 = MajoranaGroup(7, 1j, [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1])
    s_5 = MajoranaGroup(7, 1j, [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1])
    majorana_group_list=[s_0,s_1,s_2,s_3,s_4,s_5]
    majorana_code=MajoranaCode(majorana_computer,majorana_group_list)
    print(majorana_code.get_logical_operator())
