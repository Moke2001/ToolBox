import numpy as np
from Algebra.BitString.BitString import BitString
from Physics.QuantumComputation.Code.ClassicalCode.LinearCode import LinearCode


class RegularCode(LinearCode):
    """""
    self.N：int对象，比特数目
    self.codeword_vector：np.array of BitString对象，码字基矢
    self.checker_vector：np.array of BitString对象，校验子基矢
    self.number_bit：int对象，比特数目
    self.number_logical_bit：int对象，逻辑比特数目
    self.number_checker：int对象，校验子数目
    """""
    def __init__(self, number):

        ##  标准化
        assert number % 12 == 0, "n必须能被12整除"
        w_c=int(number / 4)
        w_r=int(number / 3)
        k = int(number * w_c // w_r)
        sub_rows = int(number // w_r)  # 每个子矩阵的行数
        super().__init__()

        # 生成基础子矩阵
        H_sub = np.zeros((sub_rows, number), dtype=int)
        for i in range(sub_rows):
            H_sub[i, i * w_r: (i + 1) * w_r] = 1

        # 生成置换子矩阵
        H_pre = H_sub.copy()
        np.random.seed(100)
        for _ in range(w_c - 1):  # 已包含初始矩阵，需要w_c-1次置换
            perm = np.random.permutation(number)
            H_pre = np.hstack((H_pre, H_sub[:, perm]))

        # 构建最终矩阵
        H = np.zeros((k, number), dtype=int)
        for p in range(w_c):
            row_start = p * sub_rows
            row_end = (p + 1) * sub_rows
            col_start = p * number
            col_end = (p + 1) * number
            H[row_start:row_end] = H_pre[:, col_start:col_end]
        checker_list = []
        for i in range(H.shape[0]):
            temp=BitString()
            temp.define(H[i])
            checker_list.append(temp)
        self.checkers_define(checker_list)