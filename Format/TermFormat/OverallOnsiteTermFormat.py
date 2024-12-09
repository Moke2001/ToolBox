from Format.TermFormat.TermFormat import TermFormat


class OverallOnsiteTermFormat(TermFormat):
    #%%  BLOCK：构造函数
    """""
    OverallOnsiteTerm类，定义单一两体相互作用量
    self.cell_index：格点在元胞中的序号
    self.op：格点上的算符
    OverallOnsiteTerm(label,cell_index,op,strength/[function,function_params])
    """""
    def __init__(self, label,effect, cell_index,op, *args):
        super().__init__(label,effect, *args)
        self.cell_index = cell_index
        self.op = op
    
    
    #%%  BLOCK：判断参数是否对应CouplingTerm
    def fit(self, label,*args):
        if super().fit(label):
            if self.cell_index == args[0]:
                return True
        return False
    
    
    #%%  BLOCK：获取算符对象
    def get_op(self):
        return self.op
    
    
    #%%  BLOCK：获取位置对象
    def get_unit(self):
        return self.cell_index
    
    
    # %%  BLOCK：更改算符形式
    def change(self, op, *args):
        super().change(*args)
        self.op = op
    
    
    # %%  BLOCK：复制函数
    def copy(self):
        if self.time:
            return OverallOnsiteTerm(self.label, self.cell_index, self.op, self.function, self.function_params)
        else:
            return OverallOnsiteTerm(self.label, self.cell_index, self.op, self.strength)