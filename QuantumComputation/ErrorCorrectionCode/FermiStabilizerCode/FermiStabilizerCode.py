import copy
import itertools
import galois
import numpy as np
from QuantumComputation.ErrorCorrectionCode.FermiStabilizerCode.MajoranaOperator import MajoranaOperator
from QuantumComputation.ErrorCorrectionCode.StabilizerCode import StabilizerCode


class FermiStabilizerCode(StabilizerCode):
    # %%  USER：空构造函数
    """""
    self.N：int对象，稳定子数目
    self.stabilizers：list of MajoranaOperator对象，稳定子生成元
    self.weight：int对象，编码最大能纠正的Majorana error的权重
    """""
    def __init__(self, N):
        super().__init__(N)

    #%%  USER：复制函数
    """
    output：MajoranaStabilizer对象，本对象的复制
    """
    def copy(self):
        return copy.deepcopy(self)


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
        error_list=[]
        syndrome_list=[]

        ##  遍历错误权重大小，直到发现不能纠正的错误，输出它的权重减一
        for i in range(1,self.N*2):

            """
            选取所有可能的错误位
            例如如果有3个qubits，权重为2，那么为：[(0,1),(0，2),(1,2)]
            """
            for position_list in itertools.combinations(range(self.N*2),i):
                error_temp=[0]*(self.N*2)
                for k in range(len(position_list)):
                    error_temp[position_list[k]]=1
                factor=int(i*(i-1)/2)
                if np.mod(factor,2)==0:
                    error_list.append(MajoranaOperator(1, error_temp.copy()))
                else:
                    error_list.append(MajoranaOperator(1j, error_temp.copy()))

            ##  计算所有算符的错误征状
            flag=len(syndrome_list)
            for j in range(flag,len(error_list)):
                syndrome=[]
                for k in range(len(self.stabilizers)):
                    if self.stabilizers[k].commuter(error_list[j]):
                        syndrome.append(0)
                    else:
                        syndrome.append(1)
                syndrome_list.append(syndrome)

            """
            用KL定理分析当前权重的所有错误能否被纠正
            首先计算当前错误列表的征状列表，如果它错误征状唯一则可以被纠正
            如果不唯一，则判断是否简并
            """
            for j in range(flag,len(syndrome_list)):
                if all(x==0 for x in syndrome_list):
                    if self.independent_checker(error_list[j]):
                        self.weight=weight
                        return weight
                for k in range(j):
                    if syndrome_list[j] == syndrome_list[k]:
                        temp = error_list[k].dag() * error_list[j]
                        if self.independent_checker(temp):
                            self.weight = weight
                            return weight

            ##  如果当前权重下的错误都能纠正，则将结果加一
            weight=weight+1


    # %%  USER：判断是否独立
    """
    output：bool对象，独立为True，不独立为False
    """
    def independent_checker(self, majorana_operator):
        ##  没有参数直接计算稳定子是否独立
        assert isinstance(majorana_operator, MajoranaOperator)
        code_temp = self.copy()
        code_temp.push(majorana_operator)
        check_matrix = check_matrix_generator(code_temp)

        ##  如果秩等于行数，说明确实独立
        if np.linalg.matrix_rank(check_matrix) == check_matrix.shape[0]:
            return True

        ##  如果秩不等于行数，需要根据系数进一步判断
        else:

            """
            求系数的过程
            删除当前位置上的稳定子，如果独立，说明系数为1，如果仍然不独立说明系数为0
            """
            coff_list=[]
            for i in range(len(code_temp.stabilizers)-1):
                temp = self.copy()
                temp.pop(i)
                check_matrix_temp=check_matrix_generator(temp)
                if np.linalg.matrix_rank(check_matrix_temp) == check_matrix_temp.shape[0]:
                    coff_list.append(1)
                else:
                    coff_list.append(0)

            ##  计算生成这个算符的算符的乘积系数是否一致
            eta_temp=1
            for i in range(len(coff_list)):
                if coff_list[i] == 1:
                    eta_temp=eta_temp*self.stabilizers[i].eta

            ##  如果系数一致，说明确实不独立
            if eta_temp == self.stabilizers[-1].eta:
                return False

            ##  如果系数不一致，说明仍然独立
            else:
                return True


#%%  KEY：生成一个稳定子的校验矩阵
def check_matrix_generator(stabilizer_code):
    check_matrix = np.zeros((len(stabilizer_code.stabilizers), stabilizer_code.N * 2),dtype=int)
    for i in range(len(stabilizer_code.stabilizers)):
        for j in range(len(stabilizer_code.stabilizers[i])):
            if stabilizer_code.stabilizers[i][j] == 1:
                check_matrix[i][j] = 1
    GF=galois.GF(2**1)
    check_matrix=GF(check_matrix)
    return check_matrix


if __name__ == '__main__':
    GF = galois.GF(2**1)
    A=np.array([[1,1,0],[1,1,1],[1,0,1]])
    A=GF(A)
    print(np.linalg.matrix_rank(A))