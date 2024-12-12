from Framework.Format.TermFormat.TermFormat import TermFormat


class OnsiteTermFormat(TermFormat):
    # %%  BLOCK：构造函数
    """""
    OnsiteTerm类，定义单一单体作用量
    self.position：格点位置
    self.op：格点上的算符
    OnsiteTerm(label,position,op,strength/[function,function_params])
    """""
    def __init__(self,label,effect,position,op,*args):
        super().__init__(label,effect,*args)
        self.position = position
        self.op = op
    
    
    #%%  BLOCK：判断参数是否对应OnsiteTerm
    def fit(self,label,*args):
        if super().fit(label):
            if len(args) > 0:
                if self.position==args[0]:
                    return True
        return False
    
    
    #%%  BLOCK：获取算符对象
    def get_op(self):
        return self.op
    
    
    #%%  BLOCK：获取位置对象
    def get_position(self):
        return self.position
    
    
    #%%  BLOCK：更改算符形式
    def change(self,op,*args):
        self.op=op
        super().change(*args)
    
    
    #%%  BLOCK：复制函数
    def copy(self):
        if self.time:
            return OnsiteTermFormat(self.label,self.position,self.op,self.function,self.function_params)
        else:
            return OnsiteTermFormat(self.label,self.position,self.op,self.strength)