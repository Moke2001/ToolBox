import numpy as np
from Physics.QuantumComputation.Encoder.BitString.BitString import BitString


class LinearCode:
    #%%  USER：构造函数
    """""
    self.N：int对象，比特数目
    self.codeword_vector：np.array of BitString对象，码字基矢
    self.checker_vector：np.array of BitString对象，校验子基矢
    """""
    def __init__(self):
        self.number_bit=None
        self.number_logical_bit=None
        self.number_constraint=None
        self.codeword_vector=None
        self.checker_vector=None


    #%%  USER：用码字空间基矢定义线性码
    """""
    input.codeword_vector：np.array of BitString对象，码字基矢组
    influence：给self.codeword_vector赋值，将self.checker_vector清空
    """""
    def codewords_define(self,codewords):
        ##  赋值与类型转换
        self.codeword_vector = np.empty(len(codewords), dtype=BitString)
        for i in range(len(codewords)):
            if isinstance(codewords[i],BitString):
                self.codeword_vector[i] = codewords[i]
            else:
                self.codeword_vector[i] = BitString()
                self.codeword_vector[i].define(codewords[i])
        self.codeword_vector = BitString.get_basis(self.codeword_vector)

        ##  修改原本的值
        self.checker_vector = None
        self.number_bit = self.codeword_vector[0].number_bit
        self.number_logical_bit=self.codeword_vector.shape[0]
        self.number_constraint=self.number_bit-self.number_logical_bit


    #%%  USER：用校验子空间基矢定义线性码
    """""
    input.codeword_vector：np.array of BitString对象，码字基矢组
    influence：给self.codeword_vector清空，将self.checker_vector赋值
    """""
    def checkers_define(self,checkers):
        ##  赋值与类型转换
        self.checker_vector = np.empty(len(checkers), dtype=BitString)
        for i in range(len(checkers)):
            if isinstance(checkers[i], BitString):
                self.checker_vector[i] = checkers[i]
            else:
                self.checker_vector[i] = BitString()
                self.checker_vector[i].define(checkers[i])
        self.checker_vector = BitString.get_basis(self.checker_vector)

        ##  修改原本的值
        self.codeword_vector = None
        self.number_bit = self.checker_vector[0].number_bit
        self.number_constraint = self.checker_vector.shape[0]
        self.number_logical_bit = self.number_bit - self.number_constraint


    #%%  USER：求奇偶校验子
    def get_checkers(self):
        ##  如果已经求过了，直接调用
        if self.checker_vector is not None:
            return self.checker_vector

        ##  没有求过需要重新求
        elif self.codeword_vector is not None:
            ##  构造生成矩阵
            generate_matrix=BitString.get_matrix(self.codeword_vector)

            ##  计算零空间
            null_vector_vector=generate_matrix.null_space()
            checkers_vector=np.empty(null_vector_vector.shape[0], dtype=BitString)
            for i in range(null_vector_vector.shape[0]):
                checkers_vector[i]=BitString()
                checkers_vector[i].define(null_vector_vector[i])
            self.checker_vector=checkers_vector
            return checkers_vector
        else:
            raise NotImplementedError('线性码没有初始化')


    #%%  USER：求码字
    def get_codewords(self):
        if self.codeword_vector is not None:
            return self.codeword_vector
        elif self.checker_vector is not None:
            check_matrix = BitString.get_matrix(self.checker_vector)
            null_vector_array = check_matrix.null_space()
            codeword_vector = np.empty(null_vector_array.shape[0], dtype=BitString)
            for i in range(null_vector_array.shape[0]):
                codeword_vector[i] = BitString()
                codeword_vector[i].define(null_vector_array[i])
            self.codeword_vector = codeword_vector
            return codeword_vector


    #%%  USER：求对偶码
    def get_dual_code(self):
        checker_vector=self.get_checkers()
        result=LinearCode()
        result.codewords_define(checker_vector)
        return result


    #%%  USER：检查码字是否合法
    def check(self ,bitstring):
        if isinstance(bitstring, BitString):
            checker_vector=self.get_checkers()
            for checker in checker_vector:
                if checker.inner(bitstring) != 0:
                    return False
            return True
        else:
            temp=BitString()
            temp.define(bitstring)
            return self.check(temp)


    #%%  USER：获取最大可纠错的距离
    def get_distance(self):
        codewords = self.get_codewords()
        if codewords.shape[0] == 0:
            return 0  # 空码的特殊情况

        min_weight = None
        for cw in codewords:
            # 计算当前码字的汉明重量（统计非零元素）
            weight = np.count_nonzero(cw.bit_vector)

            # 跳过全零码字
            if weight == 0:
                continue

            # 更新最小重量
            if (min_weight is None) or (weight < min_weight):
                min_weight = weight

        return min_weight if min_weight is not None else 0
