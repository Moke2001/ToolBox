import copy
import itertools
import galois
import numpy as np
from Algebra.BitString.BitString import BitString
from Algebra.Group.MajoranaGroup import MajoranaGroup


class MajoranaCode:
    # %%  USER：空构造函数
    """""
    self.N：int对象，稳定子数目
    self.stabilizers：list of PauliOperator对象，稳定子生成元
    self.weight：int对象，编码最大能纠正的Pauli error的权重
    """""
    def __init__(self):
        ##  赋值
        self.generator_vector = None
        self.number_fermion = None
        self.number_checker = 0
        self.weight = None
        self.rank=None


    # %%  USER：第一定义函数
    """
    input.checker：MajoranaGroup or list of int or np.array of int对象，稳定子生成元的格式
    input.*args：int对象，稳定子生成元的系数，默认为1
    influence：如果是第一次推送，对MajoranaCode做初始化；如果不是第一次推送，则检查fermion数目是否匹配，匹配的话推送进去
    """
    def push(self, checker, *args):
        ##  规范化操作
        if isinstance(checker, MajoranaGroup):
            checker_now = checker.copy()
            number_qubit_now = checker.number_fermion
        elif isinstance(checker, list) or isinstance(checker, np.ndarray):
            checker_now = MajoranaGroup()
            if len(args) == 0:
                checker_now.define(checker, 1)
            elif len(args) == 1:
                checker_now.define(checker, args[0])
            number_qubit_now = checker_now.number_fermion
        else:
            raise NotImplementedError('输入参数有误')

        ##  推送操作
        if self.number_checker == 0:
            self.number_checker = 1
            self.number_fermion = number_qubit_now
            self.generator_vector = np.empty(1, dtype=MajoranaGroup)
            self.generator_vector[0] = checker_now
            self.weight = None
            self.rank = None
        else:
            assert number_qubit_now == self.number_fermion, '输入的稳定子量子比特数目不符合要求'
            self.number_checker = self.number_checker + 1
            vector_now=np.empty(1, dtype=MajoranaGroup)
            vector_now[0] = checker_now
            self.generator_vector=np.append(self.generator_vector, vector_now)
            self.weight = None
            self.rank = None


    #%%  USER：检查稳定子之间是否对易
    """
    output：bool对象，编码对易性判断结果
    """
    def check_commuter(self):
        for i in range(self.generator_vector.shape[0]):
            for j in range(i+1,self.generator_vector.shape[0]):
                if not self.generator_vector[i].commuter(self.generator_vector[j]):
                    return False
        return True


    #%%  USER：计算稳定子的秩
    """
    output：int对象，稳定子生成元的秩
    """
    def get_rank(self):
        if self.rank is None:
            matrix=BitString.get_matrix(MajoranaGroup.get_bitstring(self.generator_vector))
            self.rank=np.linalg.matrix_rank(matrix)
            return self.rank
        else:
            return self.rank


    # %%  USER：计算能纠正的最大错误
    """
    output：int对象，纠错码能纠正的最大权重错误
    """
    def get_weight(self):
        ##  如果计算过了，就直接调取结果
        if self.weight is not None:
            return self.weight

        ##  如果没有计算过就计算
        weight = 0

        ##  遍历错误权重大小，直到发现不能纠正的错误，输出它的权重减一
        syndrome_list = []
        error_list = []
        for i in range(1, self.number_fermion):
            """
            选取所有可能的错误位
            例如如果有3个qubits，权重为2，那么为：[(0,1),(0，2),(1,2)]
            """
            error_position_list = itertools.combinations(range(self.number_fermion * 2), i)
            for error_position in error_position_list:
                error_temp=MajoranaGroup()
                error_temp.define(1,error_position)
                error_list.append(error_temp)

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
                    error_and_stabilizer=np.append(self.generator_vector,error_list[j])
                    if BitString.get_rank(MajoranaGroup.get_bitstring(error_and_stabilizer)) == self.get_rank()+1:
                        self.weight = weight
                        return weight
                for k in range(j):

                    ##  如果征状相同，计算是否简并
                    if syndrome_list[j] == syndrome_list[k]:
                        temp = error_list[k] * error_list[j]
                        error_and_stabilizer = np.append(self.generator_vector, temp)
                        if BitString.get_rank(MajoranaGroup.get_bitstring(error_and_stabilizer)) == self.get_rank() + 1:
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


    # %%  USER：计算编码率
    """
    output：float对象，纠错码的编码率
    """
    def get_ratio(self):
        return (self.number_fermion - len(self.generator_vector)) / self.number_fermion


    #%%  USER：获取逻辑算符
    """
    output：np.array对象，和纠错码对易且独立的逻辑算符数组
    """
    def get_logical_operator(self):
        ##  构造校验矩阵
        check_matrix=np.zeros((self.number_fermion * 6, self.number_fermion * 2), dtype=int)
        for i in range(self.generator_vector.shape[0]):
            for j in range(self.number_fermion * 2):
                check_matrix[i, j] = self.generator_vector[i][j]
        GF = galois.GF(2)
        check_matrix = GF(check_matrix)

        # 计算原始零空间基矢
        null_space = check_matrix.null_space()
        zeros_vector=GF(np.zeros(self.number_fermion * 2, dtype=int))

        # 筛选与行空间无关的基矢
        independent_null_basis_list=[]
        for vec in null_space:
            number=len(independent_null_basis_list)
            rank_before = np.linalg.matrix_rank(check_matrix)
            check_matrix[number+self.generator_vector.shape[0]+1,:]=GF(np.array(vec,dtype=int))
            if np.linalg.matrix_rank(check_matrix)==rank_before+1:
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
