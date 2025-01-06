import copy
import itertools
from sre_constants import error

import galois
import numpy as np
from QuantumComputation.ErrorCorrectionCode.PauliStabilizerCode.PauliOperator import PauliOperator
from QuantumComputation.ErrorCorrectionCode.StabilizerCode import StabilizerCode


class PauliStabilizerCode(StabilizerCode):
    # %%  USER：空构造函数
    """""
    self.N：int对象，稳定子数目
    self.stabilizers：list of PauliOperator对象，稳定子生成元
    self.weight：int对象，编码最大能纠正的Pauli error的权重
    """""
    def __init__(self,N):
        super().__init__(N)


    #%%  USER：计算能纠正的最大错误
    def get_weight(self):
        ##  如果计算过了，就直接调取结果
        if self.weight is not None:
            return self.weight

        ##  如果没有计算过就计算
        weight=0

        ##  遍历错误权重大小，直到发现不能纠正的错误，输出它的权重减一
        syndrome_list=[]
        error_list=[]
        for i in range(1,self.N):

            """
            所有可能的错误位上的错误串
            例如如果当前权重为2，则错误串为：[XX,XY,XZ,...,ZZ]
            错误串后面填入所有可能的错误位上
            """
            params = ()  # 错误串直积表
            for j in range(i):
                params=params+(['X','Y','Z'],)

            """
            选取所有可能的错误位
            例如如果有3个qubits，权重为2，那么为：[(0,1),(0，2),(1,2)]
            """
            for position_list in itertools.combinations(range(self.N),i):
                error_string=['I']*self.N  # 错误初始化
                for error_words in itertools.product(*params):
                    for k in range(len(position_list)):
                        error_string[position_list[k]]=error_words[k]
                    error_list.append(PauliOperator(1,error_string.copy()))

            """
            用KL定理分析当前权重的所有错误能否被纠正
            首先计算当前错误列表的征状列表，如果它错误征状唯一则可以被纠正
            如果不唯一，则判断是否简并
            """
            flag=len(syndrome_list)  # 当前征状列表长度
            for j in range(flag,len(error_list)):
                syndrome_temp=[]
                for k in range(len(self.stabilizers)):
                    if self.stabilizers[k].commuter(error_list[j]):
                        syndrome_temp.append(0)
                    else:
                        syndrome_temp.append(1)
                syndrome_list.append(syndrome_temp)

            ##  查找征状相同的错误
            for j in range(flag,len(syndrome_list)):

                ##  如果全为0，要判断在不在稳定子内
                if all(x==0 for x in syndrome_list):
                    if self.independent_checker(error_list[j]):
                        self.weight=weight
                        return weight
                for k in range(j):

                    ##  如果征状相同，计算是否简并
                    if syndrome_list[j]==syndrome_list[k]:
                        temp=error_list[k]*error_list[j]
                        if self.independent_checker(temp):
                            self.weight = weight
                            return weight

            ##  如果当前权重下的错误都能纠正，则将结果加一
            weight=weight+1


    #%%  USER：复制函数
    """
    output：PauliStabilizer对象，本对象的复制
    """
    def copy(self):
        return copy.deepcopy(self)


    #%%  USER：判断是否独立
    """
    output：bool对象，独立为True，不独立为False
    """
    def independent_checker(self,*args):
        ##  没有参数，判断当前稳定子生成元是否独立
        if len(args)==0:

            ##  计算校验矩阵
            check_matrix=np.zeros((len(self.stabilizers),self.N*2),dtype=int)
            for i in range(len(self.stabilizers)):
                for j in range(self.N):
                    if self.stabilizers[i][j]=='X':
                        check_matrix[i][j]=1
                    elif self.stabilizers[i][j]=='Z':
                        check_matrix[i][j+self.N]=1
                    elif self.stabilizers[i][j]=='Y':
                        check_matrix[i][j+self.N]=1
                        check_matrix[i][j]=1
                    elif self.stabilizers[i][j]=='I':
                        pass

            ##  计算校验矩阵的01域上的形式
            GF=galois.GF(2**1)
            check_matrix=GF(check_matrix)

            ##  根据矩阵01秩计算是否独立
            if np.linalg.matrix_rank(check_matrix)==check_matrix.shape[0]:
                return True
            else:
                return False

        ##  如果有参数，则需要判断新算符是否与其他稳定子独立
        elif len(args)==1:
            assert isinstance(args[0],PauliOperator)

            ##  如果系数不是1，那么一定不能被稳定子表示
            if args[0].eta!=1:
                return True

            ##  如果系数是1，那么添加进去再判断
            else:
                code_temp=self.copy()
                code_temp.push(args[0])
                return code_temp.independent_checker()

        ##  其他参数数目抛出错误
        else:
            raise ValueError("Incorrect number of arguments")



