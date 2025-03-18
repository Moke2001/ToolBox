import copy
import numpy as np
from Physics.QuantumComputation.StabilizerSimulator.Group.Group import Group


class MajoranaGroup(Group):
    #%%  USER：构造函数
    """""
    Majorana Group的表示，这个类包含了所有参数N不同的Majorana group中的元素
    self.N：int对象，Fermionic sites的数目
    self.majorana_vector：np.array of int对象，用于表示对应位上算符存在性的一阶张量
    例如[1,0,0,1]代表了$\hat\gamma_0\hat\gamma_1'$
    self.coff：complex对象，只能为1，-1，1j，-1j四个数值的系数
    """""
    def __init__(self,N,coff,majorana_vector):
        super().__init__(N)
        assert self.N*2==len(majorana_vector)
        self.majorana_vector=np.array(majorana_vector, dtype=int)
        self.coff=coff


    #%%  USER：重载乘法运算符
    """
    input.other：MajoranaGroup对象或complex对象或int对象，右边乘上的对象
    output：MajoranaGroup对象，乘出来的结果
    """
    def __mul__(self,other):
        ##  如果对方是MajoranaGroup对象
        if isinstance(other, MajoranaGroup):
            assert len(self.majorana_vector) == len(self.majorana_vector)  # 只有同群才能相乘

            ##  计算相乘结果
            majorana_vector_new = np.zeros_like(self.majorana_vector,dtype=int)
            new_coff = self.coff * other.coff

            """
            如果对方的算符是1，将对方的算符依次替换到前面，直到到达对应位置上
            替换过程中如果经过一个1，符号要发生一次变化
            如果对方的算符是0，那么不需要替换
            """
            for i in range(len(other.majorana_vector)):
                if other.majorana_vector[i] == 0:
                    majorana_vector_new[i] = self.majorana_vector[i]
                else:
                    for j in range(len(self.majorana_vector) - 1, i, -1):
                        if self.majorana_vector[i] == 1:
                            new_coff = -new_coff
                    if self.majorana_vector[i] == 0:
                        majorana_vector_new[i]=1
                    else:
                        majorana_vector_new[i]=0
            return MajoranaGroup(self.N,new_coff,majorana_vector_new)

        ##  如果对方是数，则与系数直接计算
        elif isinstance(other, complex) or isinstance(other, int):
            result = self.copy()
            result.coff = self.coff * other
            return result


    # %%  USER：重载乘法运算符
    """
    input.other：MajoranaGroup对象或complex对象或int对象，右边乘上的对象
    output：MajoranaGroup对象，乘出来的结果
    """
    def __rmul__(self,other):
        if isinstance(other, MajoranaGroup):
            return other.__mul__(other)
        elif isinstance(other, complex) or isinstance(other, int):
            return self.__mul__(other)


    # %%  USER：重载等于号运算符
    """
    input.other：any对象，只有MajoranaGroup对象才有可能相等
    output：bool对象，判断结果
    """
    def __eq__(self, other):
        if isinstance(other, MajoranaGroup):
            if self.N==other.N:
                if np.all(self.majorana_vector == other.majorana_vector):
                    return True
        return False


    # %%  USER：复制函数
    """
    output：MajoranaGroup对象，复制结果
    """
    def copy(self):
        return copy.deepcopy(self)


    # %%  USER：算符共轭
    """
    output：MajoranaOperator对象，共轭结果
    """
    def dag(self):
        num = len([item for item in self.majorana_vector if item == 1])
        factor = (-1)**(num * (num - 1) / 2)
        if self.coff==1 or self.coff==-1:
            result = self.copy()
            result.coff=result.coff*factor
            return result
        else:
            result=self.copy()
            result.coff=-result.coff*factor
            return result


    #%%  USER：计算权重
    """
    output：int对象，含有1的个数
    """
    def get_weight(self):
        weight=0
        for i in range(self.N*2):
            weight=weight+self.majorana_vector[i]
        return weight


    # %%  USER：对易式
    """
    output：bool对象，是否对易的判断
    """
    def commuter(self, other):
        ##  标准化步骤
        assert isinstance(other, MajoranaGroup), 'Other参数必须是MajoranaOperator对象'
        assert (self.N == other.N), '稳定子字符串长度必须与sites数目相同'

        ##  根据对易关系计算两个算符之间的对易性
        result=0
        for i in range(other.N*2):
            result=result+self.majorana_vector[i]*other.majorana_vector[i]
        factor=result+self.get_weight()*other.get_weight()

        ##  返回结果
        return np.mod(factor,2)==0


    #%%  USER：获取第item个位置上的算符
    def __getitem__(self, item):
        if isinstance(item,int):
            return self.majorana_vector[item]
        elif isinstance(item,tuple):
            index_0=item[0]
            index_1=item[1]
            return self.majorana_vector[index_0 * 2 + index_1]