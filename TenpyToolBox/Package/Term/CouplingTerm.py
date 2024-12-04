from TenpyToolBox.Package.Term.Term import Term


class CouplingTerm(Term):
    #%%  BLOCK：构造函数
    """""
    CouplingTerm类，定义单一两体相互作用量
    self.position_0：第一个格点位置
    self.position_1：第二个格点位置
    self.op_0：第一个格点上的算符
    self.op_1：第二个格点上的算符
    CouplingTerm(label,position_0,position_1,op_0,op_1,strength/[function,function_params])
    """""
    def __init__(self, label, position_0, position_1, op_0, op_1, *args):
        super().__init__(label, *args)
        self.position_0 = position_0
        self.position_1 = position_1
        self.op_0 = op_0
        self.op_1 = op_1


    #%%  BLOCK：判断参数是否对应CouplingTerm
    def fit(self, label, *args):
        if super().__eq__(label):
            if len(args) >= 2:
                if self.position_0 == args[0] and self.position_1 == args[1]:
                    return True
        return False


    #%%  BLOCK：获取算符对象
    def get_op(self):
        return self.op_0, self.op_1


    #%%  BLOCK：获取位置对象
    def get_position(self):
        return self.position_0, self.position_1


    #%%  BLOCK：更改算符形式
    def change(self, op_0, op_1, *args):
        super().change(*args)
        self.op_0 = op_0
        self.op_1 = op_1


    #%%  BLOCK：复制函数
    def copy(self):
        if self.time:
            return CouplingTerm(self.label, self.position_0, self.position_1, self.op_0, self.op_1, self.function,
                self.function_params)
        else:
            return CouplingTerm(self.label, self.position_0, self.position_1, self.op_0, self.op_1, self.strength)
