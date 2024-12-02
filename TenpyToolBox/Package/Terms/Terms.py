from TenpyToolBox.Package.Term.CouplingTerm import CouplingTerm
from TenpyToolBox.Package.Term.MultiTerm import MultiTerm
from TenpyToolBox.Package.Term.OnsiteTerm import OnsiteTerm
from TenpyToolBox.Package.Term.OverallCouplingTerm import OverallCouplingTerm
from TenpyToolBox.Package.Term.OverallMultiTerm import OverallMultiTerm
from TenpyToolBox.Package.Term.OverallOnsiteTerm import OverallOnsiteTerm
from TenpyToolBox.Package.Term.Term import Term


class Terms:
    #%%  BLOCK：构造函数
    """""
    Terms对象的构造函数，一个空构造函数
    self.terms：list of Term对象，储存模型的作用量
    self.number：int对象，储存作用量个数
    TermList对象初始化后通过调用push函数等再进行实例化
    """""
    def __init__(self):
        self.terms = []
        self.number=0
        

    #%%  BLOCK：按terms序号返回Term对象
    def get_term(self,index:int):
        return self.terms[index]
    
    
    #%%  BLOCK：Term对象推送到terms
    def push(self, term:Term):
        assert isinstance(term,Term),'term must be of type Term'
        self.terms.append(term)
        self.number+=1
    
    
    #%%  BLOCK：按terms序号删除Term对象
    def pull(self,index:int):
        self.terms.pop(index)
        self.number-=1
    
    
    #%%  BLOCK：按Term对象内容改变terms中的Term对象
    """
    Terms中的Term对象的基本形式：标序位符值
    OnsiteTerm(label,position,op,strength/[function,function_params])
    CouplingTerm(label,position_0,positon_1,op_0,op_1,strength/[function,function_params])
    MultiTerm(label,position_list,op_list,strength/[function,function_params])
    OverallOnsiteTerm(label,cell_index,op,strength/[function,function_params])
    OverallCouplingTerm(label,cell_index_0,cell_index_1,vector,op_0,op_1,strength/[function,function_params])
    OverallMultiTerm(label,cell_index_list,vector_list,op_list,strength/[function,function_params])
    """
    def change(self,*args):
        type=Terms.judge_type(*args)
        term_index=self.find(*args)  # 寻找输入参数对应Term对象所在terms的序号
        self.terms[term_index]=type(*args)  # 根据输入变化做改变
    
    #%%  BLOCK：按Term对象内容删除terms中的Term对象
    def remove(self,*args):
        term_index=self.find(*args)  # 寻找输入参数对应Term对象所在terms的序号
        self.terms.pop(term_index)

    
    #%%  BLOCK：在terms中寻找特定Term对象
    """
    find函数只按照标签、序号和位置寻找特定的Term对象，不考虑强度
    """
    def find(self,*args):
        for i in range(len(self.terms)):
            if self.terms[i].fit(*args):
                return i
        return None
    
    
    #%%  BLOCK：清空terms函数
    def clear(self):
        self.terms = []
        self.number=0
    
    
    #%%  BLOCK：Term对象类型判断函数
    """
    根据输入参数的形式判断输入的参数对应的Term对象类型，只根据序号、位置的形式来判断
    judge_type是一个静态函数
    """
    @staticmethod
    def judge_type(*args):
        ##  OnsiteTerm
        if isinstance(args[1],tuple) and isinstance(args[2],str):
            return OnsiteTerm
        ##  CouplingTerm
        elif isinstance(args[1],tuple) and isinstance(args[2],tuple):
            return CouplingTerm
        ##  OverallOnsiteTerm
        elif isinstance(args[1],int) and isinstance(args[2],str):
            return OverallOnsiteTerm
        ##  OverallCouplingTerm
        elif isinstance(args[1],int) and isinstance(args[2],int):
            return OverallCouplingTerm
        elif isinstance(args[1],list) and isinstance(args[2],list):
            ##  OverallMultiTerm
            if isinstance(args[1][0],tuple):
                return MultiTerm
            ##  MultiTerm
            else:
                return OverallMultiTerm
        else:
            raise TypeError('Type is not supported')