from Framework.Term.Term import Term


class OverallCouplingTerm(Term):
    #%%  BLOCK：构造函数
    """""
    OverallCouplingTerm类，定义单一两体相互作用量
    self.cell_index_0：第一个格点所在元胞序号
    self.cell_index_1：第二个格点所在元胞序号
    self.vector：两个元胞的相对格位移
    self.op_0：第一个格点上的算符
    self.op_1：第二个格点上的算符
    OverallCouplingTerm(label,cell_index_0,cell_index_1,op_0,op_1,strength/[function,function_params])
    """""
    def __init__(self, label,effect, cell_index_0,cell_index_1,vector,op_0,op_1, *args):
        super().__init__(label,effect, *args)
        self.cell_index_0 = cell_index_0
        self.cell_index_1 = cell_index_1
        self.vector = vector
        self.op_0 = op_0
        self.op_1 = op_1
    
    
    #%%  BLOCK：判断参数是否对应CouplingTerm
    def fit(self, label,*args):
        if super().fit(label):
            if self.cell_index_0 == args[0] and self.cell_index_1 == args[1] and self.vector == args[2]:
                return True
        return False
    
    
    #%%  BLOCK：获取算符对象
    def get_op(self):
        return self.op_0,self.op_1
    
    
    #%%  BLOCK：获取位置对象
    def get_unit(self):
        return self.cell_index_0,self.cell_index_1,self.vector
    
    
    #%%  BLOCK：更改算符形式
    def change(self, op_0,op_1, *args):
        super().change(*args)
        self.op_0 = op_0
        self.op_1 = op_1
    
    
    #%%  BLOCK：复制函数
    def copy(self):
        if self.time:
            return OverallCouplingTerm(self.label, self.cell_index_0,self.cell_index_1, self.op_0,self.op_1, self.function, self.function_params)
        else:
            return OverallCouplingTerm(self.label, self.cell_index_0,self.cell_index_1, self.op_0,self.op_1, self.strength)
