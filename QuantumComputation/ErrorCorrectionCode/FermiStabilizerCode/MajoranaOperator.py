import copy

import galois
import numpy as np


class MajoranaOperator:
    #%%  USER：Majorana算符类的生成函数
    def __init__(self, eta, majorana_string):
        ##  校验
        assert eta==1 or eta==-1 or eta==1j or eta==-1j

        ##  赋值
        self.majorana_string = majorana_string
        self.eta = eta


    #%%  USER：重载乘法运算符
    """
    input.other：int or complex or float or MajoranaOperator对象，本对象右边乘的对象
    output.result：MajoranaOperator对象，乘积结果
    """
    def __mul__(self, other):
        ##  如果对方是PauliOperator对象
        if isinstance(other, MajoranaOperator):

            ##  校验
            assert len(self.majorana_string) == len(self.majorana_string)

            ##  计算相乘结果
            new_pauli_string = []
            new_eta=self.eta*other.eta

            """
            如果对方的算符是1，将对方的算符依次替换到前面，直到到达对应位置上
            替换过程中如果经过一个1，符号要发生一次变化
            如果对方的算符是0，那么不需要替换
            """
            for i in range(len(other.majorana_string)):
                if other.majorana_string[i]==0:
                    new_pauli_string.append(self.majorana_string[i])
                else:
                    for j in range(len(self.majorana_string)-1,i,-1):
                        if self.majorana_string[i]==1:
                            new_eta=-new_eta
                    if self.majorana_string[i]==0:
                        new_pauli_string.append(1)
                    else:
                        new_pauli_string.append(0)

            ##  返回结果
            return MajoranaOperator(new_eta, new_pauli_string)

        ##  如果对方是数，则与系数直接计算
        elif isinstance(other, complex) or isinstance(other, int):
            new_pauli_string = self.majorana_string.copy()
            return MajoranaOperator(self.eta * other, new_pauli_string)


    #%%  USER：重载乘法运算符
    """
    input.other：int or complex or float or MajoranaOperator对象，本对象右边乘的对象
    output.result：MajoranaOperator对象，乘积结果
    """
    def __rmul__(self, other):
        if isinstance(other, MajoranaOperator):
            return other.__mul__(self)
        elif isinstance(other, complex) or isinstance(other, int):
            return self.__mul__(other)


    #%%  USER：重载长度运算符
    """
    output：int对象，self.majorana_string的长度
    """
    def __len__(self):
        return len(self.majorana_string)


    #%%  USER：取值运算符
    """
    output：str对象，self.majorana_string[item]
    """
    def __getitem__(self, item):
        return self.majorana_string[item]


    #%%  USER：复制函数
    """
    output：MajoranaOperator对象，复制结果
    """
    def copy(self):
        return copy.deepcopy(self)


    # %%  USER：算符共轭
    """
    output：MajoranaOperator对象，共轭结果
    """
    def dag(self):
        num = len([item for item in self.majorana_string if item == 1])
        factor = (-1)**(num * (num - 1) / 2)
        if self.eta==1 or self.eta==-1:
            result = self.copy()
            result.eta=result.eta*factor
            return result
        else:
            result=self.copy()
            result.eta=-result.eta*factor
            return result


    # %%  USER：计算对易式
    """
    input.g_0：list of int对象，Majorana算符字符串
    input.g_1：list of int对象，Majorana算符字符串
    output.flag：bool对象，对易则为True
    """
    def commuter(self,other):
        ##  标准化步骤
        assert isinstance(other, MajoranaOperator),'Other参数必须是MajoranaOperator对象'
        assert (len(self) == len(other)), '稳定子字符串长度必须与sites数目相同'

        ##  根据对易关系计算两个算符之间的对易性
        flag = True
        for i in range(len(other)):
            if other[i]!=0:
                for j in range(len(self)):
                    if self[i] == 1 and i != j:
                        flag = not flag

        ##  返回结果
        return flag