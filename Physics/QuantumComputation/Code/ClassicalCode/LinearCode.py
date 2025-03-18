import numpy as np
from Algebra.BitString.BitString import BitString


class LinearCode:
    #%%  USER：构造函数
    """""
    self.N：int对象，比特数目
    self.codeword_vector：np.array of BitString对象，码字基矢
    self.checker_vector：np.array of BitString对象，校验子基矢
    self.number_bit：int对象，比特数目
    self.number_logical_bit：int对象，逻辑比特数目
    self.number_checker：int对象，校验子数目
    """""
    def __init__(self):
        self.number_bit=None
        self.number_logical_bit=None
        self.number_checker=None
        self.codeword_vector=None
        self.checker_vector=None


    #%%  USER：推送码字定义函数
    def push_codeword(self,codeword):
        if self.codeword_vector is None:
            codeword_now=BitString()
            codeword_now.define(codeword)
            self.codeword_vector=np.empty(1,dtype=BitString)
            self.codeword_vector[0]=codeword_now
            self.number_bit=codeword_now.number_bit
            self.checker_vector=None
            self.number_logical_bit=None
            self.number_checker=None
        else:
            codeword_now=BitString()
            codeword_now.define(codeword)
            assert self.number_bit==codeword_now.number_bit
            self.codeword_vector=np.append(self.codeword_vector,codeword_now)
            self.checker_vector=None
            self.number_logical_bit=None
            self.number_checker=None


    #%%  USER：推送校验子定义函数
    def push_checker(self,checker):
        if self.checker_vector is None:
            checker_now=BitString()
            checker_now.define(checker)
            self.checker_vector=np.empty(1,dtype=BitString)
            self.checker_vector[0]=checker_now
            self.number_bit=checker_now.number_bit
            self.codeword_vector=None
            self.number_logical_bit=None
            self.number_checker=None
        else:
            checker_now=BitString()
            checker_now.define(checker)
            assert self.number_bit==checker_now.number_bit
            vector_now=np.empty(1,dtype=BitString)
            vector_now[0]=checker_now
            self.checker_vector=np.append(self.checker_vector,vector_now)
            self.codeword_vector=None
            self.number_logical_bit=None
            self.number_checker=None


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

        ##  修改原本的值
        self.checker_vector = None
        self.number_bit = self.codeword_vector[0].number_bit
        self.number_logical_bit=None
        self.number_checker=None


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

        ##  修改原本的值
        self.codeword_vector = None
        self.number_bit = self.checker_vector[0].number_bit
        self.number_logical_bit=None
        self.number_checker=None


    #%%  USER：求奇偶校验子
    def get_checkers(self):
        ##  如果已经求过了，直接调用
        if self.checker_vector is not None:
            return BitString.get_basis(self.checker_vector)

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
            self.number_checker=checkers_vector.shape[0]
            self.number_logical_bit=self.number_bit-self.number_checker
            return checkers_vector
        else:
            raise NotImplementedError('线性码没有初始化')


    #%%  USER：求码字
    def get_codewords(self):
        if self.codeword_vector is not None:
            return BitString.get_basis(self.codeword_vector)
        elif self.checker_vector is not None:
            check_matrix = BitString.get_matrix(self.checker_vector)
            null_vector_array = check_matrix.null_space()
            codeword_vector = np.empty(null_vector_array.shape[0], dtype=BitString)
            for i in range(null_vector_array.shape[0]):
                codeword_vector[i] = BitString()
                codeword_vector[i].define(null_vector_array[i])
            self.codeword_vector = codeword_vector
            self.number_logical_bit=codeword_vector.shape[0]
            self.number_checker=self.number_bit-self.number_logical_bit
            return codeword_vector


    #%%  USER：求对偶码
    def get_dual_code(self):
        checker_vector=self.get_checkers()
        result=LinearCode()
        result.codewords_define(checker_vector)
        return result


    #%%  USER：判断对偶性质
    def dual_judge(self):
        dual_code=self.get_dual_code()
        codewords=self.get_codewords()
        dual_codewords=dual_code.get_codewords()
        if len(dual_codewords)>len(codewords):
            for i in range(len(codewords)):
                if not BitString.independent_judge(np.append(dual_codewords,codewords[i])):
                    return 'None'
            return 'Weakly Self Dual'
        elif len(dual_codewords)<len(codewords):
            for i in range(len(dual_codewords)):
                if not BitString.independent_judge(np.append(codewords,dual_codewords[i])):
                    return 'None'
            return 'Dual Containing'
        else:
            for i in range(len(dual_codewords)):
                if not BitString.independent_judge(np.append(codewords,dual_codewords[i])):
                    return 'None'
            return 'Self Dual'


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


