import numpy as np
from Physics.QuantumComputation.Encoder.BitString.BitString import BitString
from Physics.QuantumComputation.Encoder.Code.ClassicalCode.LinearCode import LinearCode


class RegularCode(LinearCode):
    def __init__(self,n):
        assert n % 12 == 0, "n必须能被12整除"
        w_c=int(n/4)
        w_r=int(n/3)
        k = int(n * w_c // w_r)
        sub_rows = int(n // w_r)  # 每个子矩阵的行数
        super().__init__()

        # 生成基础子矩阵
        H_sub = np.zeros((sub_rows, n), dtype=int)
        for i in range(sub_rows):
            H_sub[i, i * w_r: (i + 1) * w_r] = 1

        # 生成置换子矩阵
        H_pre = H_sub.copy()
        np.random.seed(100)
        for _ in range(w_c - 1):  # 已包含初始矩阵，需要w_c-1次置换
            perm = np.random.permutation(n)
            H_pre = np.hstack((H_pre, H_sub[:, perm]))

        # 构建最终矩阵
        H = np.zeros((k, n), dtype=int)
        for p in range(w_c):
            row_start = p * sub_rows
            row_end = (p + 1) * sub_rows
            col_start = p * n
            col_end = (p + 1) * n
            H[row_start:row_end] = H_pre[:, col_start:col_end]
        checker_list = []
        for i in range(H.shape[0]):
            temp=BitString()
            temp.define(H[i])
            checker_list.append(temp)
        self.checkers_define(checker_list)