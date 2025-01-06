import copy


class PauliOperator:
    #%%  USER：Pauli群算符生成函数
    """"
    self.eta：int or complex对象，算符系数
    self.pauli_string：list of str对象，对应每个qubit的算符
    """""
    def __init__(self, eta, pauli_string):
        ##  校验
        assert eta==1 or eta==-1 or eta==1j or eta==-1j,'系数必须是四元数'

        ##  赋值
        self.pauli_string = pauli_string
        self.eta = eta


    #%%  USER：重载乘法运算符
    """
    input.other：int or complex or float or PauliOperator对象，本对象右边乘的对象
    output.result：PauliOperator对象，乘积结果
    """
    def __mul__(self, other):
        ##  如果对方是PauliOperator对象
        if isinstance(other, PauliOperator):

            ##  校验二者qubit数目相同
            assert len(self.pauli_string)==len(self.pauli_string)

            ##  计算相乘结果
            new_pauli_string = []  # 新算符每位上的Pauli算符列表
            new_eta=self.eta*other.eta  # 新算符的系数

            """
            对每一位上的Pauli算符逐个相乘并计算对应位上的算符结果和系数结果
            局域Pauli算符之间是对易的，因此可以逐位计算
            例如X_0Y_1Z_2*Y_0I_1X_2=(X_0Y_0)*Y_1*(Z_2X_2)
            """
            for i in range(len(self.pauli_string)):

                ##  本体这一位等于I
                if self.pauli_string[i]=='I':
                    new_pauli_string.append(other.pauli_string[i])

                ##  对方这一位等于I
                if other.pauli_string[i]=='I':
                    new_pauli_string.append(self.pauli_string[i])

                ##  本体这一位等于X
                elif self.pauli_string[i]=='X':
                    if other.pauli_string[i]=='X':
                        new_pauli_string.append('I')
                    elif other.pauli_string[i]=='Y':
                        new_pauli_string.append('Z')
                        new_eta=new_eta*1j
                    elif other.pauli_string[i]=='Z':
                        new_pauli_string.append('Y')
                        new_eta=new_eta*1j

                ##  本体这一位等于Y
                elif self.pauli_string[i]=='Y':
                    if other.pauli_string[i]=='I':
                        new_pauli_string.append('Y')
                    elif other.pauli_string[i]=='X':
                        new_pauli_string.append('Z')
                        new_eta = new_eta * (-1j)
                    elif other.pauli_string[i]=='Y':
                        new_pauli_string.append('I')
                    elif other.pauli_string[i]=='Z':
                        new_pauli_string.append('X')
                        new_eta=new_eta*1j

                ##  本体这一位等于Z
                elif self.pauli_string[i]=='Z':
                    if other.pauli_string[i]=='I':
                        new_pauli_string.append('Z')
                    elif other.pauli_string[i]=='X':
                        new_pauli_string.append('Y')
                        new_eta = new_eta * (-1j)
                    elif other.pauli_string[i]=='Y':
                        new_pauli_string.append('X')
                        new_eta = new_eta * (-1j)
                    elif other.pauli_string[i]=='Z':
                        new_pauli_string.append('I')

            ##  返回结果
            return PauliOperator(new_eta, new_pauli_string)

        ##  如果对方是数，则与系数直接计算
        elif isinstance(other, complex) or isinstance(other, int) or isinstance(other, float):
            new_pauli_string = self.pauli_string.copy()
            return PauliOperator(self.eta*other, new_pauli_string)


    #%%  USER：重载乘法运算符
    """
    input.other：int or complex or float or PauliOperator对象，本对象右边乘的对象
    output.result：PauliOperator对象，乘积结果
    """
    def __rmul__(self, other):
        if isinstance(other, PauliOperator):
            return other.__mul__(self)
        elif isinstance(other, complex) or isinstance(other, int):
            return self.__mul__(other)


    #%%  USER：重载长度运算符
    """
    output：int对象，self.pauli_string的长度
    """
    def __len__(self):
        return len(self.pauli_string)


    #%%  USER：取值运算符
    """
    output：str对象，self.pauli_string[item]
    """
    def __getitem__(self, item):
        return self.pauli_string[item]


    #%%  USER：复制函数
    """
    output：PauliOperator对象，复制结果
    """
    def copy(self):
        return copy.deepcopy(self)


    # %%  USER：算符共轭
    """
    output：PauliOperator对象，共轭结果
    """
    def dag(self):
        if self.eta==1 or self.eta==-1:
            return self.copy()
        else:
            result=self.copy()
            result.eta=-self.eta
            return result


    #%%  USER：对易式
    def commuter(self, other):
        temp_0 = self*other
        temp_1 = other*self
        return temp_0.eta==temp_1.eta
