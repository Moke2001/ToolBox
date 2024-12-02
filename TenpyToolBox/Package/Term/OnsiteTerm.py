from TenpyToolBox.Package.Term.Term import Term


class OnsiteTerm(Term):
    ##  构造函数
    def __init__(self,label,position,op,*args):
        super().__init__(label,*args)
        self.position = position
        self.op = op
    
    ##  判断相等函数
    def fit(self,label,*args):
        if super().fit(label):
            if self.position==args[0]:
                return True
        return False
    
    ##  获取算符函数
    def get_op(self):
        return self.op
    
    ##  获取位置函数
    def get_position(self):
        return self.position
    
    ##  更改算符
    def change(self,op,*args):
        self.op=op
        super().change(*args)
    
    ##  复制函数
    def copy(self):
        if self.time:
            return OnsiteTerm(self.label,self.position,self.op,self.function,self.function_params)
        else:
            return OnsiteTerm(self.label,self.position,self.op,self.strength)