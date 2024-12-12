import copy
from qutip import Qobj
from tenpy import MPS
from Data.StateMPSTools.StateMPS import mps_expectation, mps_apply, mps_overlap
from Data.StateTools.Stack2MPS import stack2mps
from Data.StateTools.Stack2Vector import stack2vector
from Data.StateVectorTools.VectorApply import vector_apply
from Data.StateVectorTools.VectorExpectation import vector_expectation
from Data.StateVectorTools.VectorOverlap import vector_overlap
from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.Format.TermFormat.TermFormat import TermFormat
from Framework.Format.TermFormat.TermsFormat import TermsFormat
from Framework.ModelPreparer.ModelPreparer import model_preparer


class State:
    #%%  BLOCK：构造函数
    def __init__(self,*args):
        ##  空构造函数
        if len(args) == 0:
            self.stack = None
            self.mps = None
            self.vector = None

        ##  其他构造函数
        else:
            raise NotImplemented


    #%%  BLOCK：初始化函数
    def initial(self,arg):
        if isinstance(arg,list):
            self.stack = arg
            self.vector = None
            self.mps = None
        elif isinstance(arg,Qobj):
            self.vector = arg
            self.mps = None
            self.stack = None
        elif isinstance(arg,MPS):
            self.mps = arg
            self.stack = None
            self.vector = None


    #%%  BLOCK：强制初始化函数，正确性由上级保证
    def initial_force(self,stark,vector,mps):
        self.stack=stark
        self.vector = vector
        self.mps = mps


    #%%  BLOCK：检查函数，判断有没有初始化
    def check(self):
        return self.stack is not None or self.mps is not None or self.vector is not None


    #%%  BLOCK：取消效用函数，将某个数据标记为无效
    def invalidate(self,arg):
        if arg=='stack':
            self.stack = None
        elif arg=='mps':
            self.mps = None
        elif arg=='vector':
            self.vector = None
        else:
            raise ValueError


    #%%  BLOCK：效用函数，将某个数据根据其他有效数据初始化
    def validate(self,model,arg):

        ##  判断态矢是否有效
        if self.check():

            ##  对队列做有效化
            if arg=='stack':
                if self.stack is not None:
                    print('不需要重复有效化，请检查')
                elif self.mps is not None:
                    raise NotImplemented
                elif self.vector is not None:
                    raise NotImplemented
                else:
                    pass

            ##  对vector做有效化
            elif arg=='vector':
                if self.vector is not None:
                    print('不需要重复有效化，请检查')
                elif self.mps is not None:
                    raise NotImplemented
                elif self.stack is not None:
                    self.vector = stack2vector(model,self.stack)
                else:
                    pass

            ##  对mps做有效化
            elif arg=='mps':
                if self.mps is not None:
                    print('不需要重复有效化，请检查')
                elif self.stack is not None:
                    self.mps = stack2mps(model,self.stack)
                elif self.vector is not None:
                    raise NotImplemented
                else:
                    pass

            ##  抛出未实现错误
            else:
                raise NotImplementedError


    #%%  BLOCK：返回MPS对象
    def get_mps(self,model):
        self.validate('mps',model)
        return self.mps


    #%%  BLOCK：返回vector对象
    def get_vector(self,model):
        self.validate('vector',model)
        return self.vector


    #%%  BLOCK：返回stack格式对象
    def get_stack(self,model):
        self.validate('stack',model)
        return self.stack


    #%%  BLOCK：重载加法运算符
    def __add__(self, other):
        assert isinstance(other, State), '只能对算符对象做加法'
        assert self.check() and other.check(),'算符必须已经初始化'

        ##  实现队列相加
        if self.stack is not None and other.stack is not None:
            stack=self.stack + other.stack
        else:
            stack=None

        ##  实现MPS之间的加法
        if self.mps is not None and other.mps is not None:
            mps=self.mps.add(other.mps,1,1)
        else:
            mps=None

        ##  实现矩阵相加
        if self.vector is not None and other.vector is not None:
            vector=self.vector + other.vector
        else:
            vector=None

        ##  构造并返回结果对象
        new_object=State()
        new_object.initial_force(stack,vector,mps)
        if new_object.check():
            return new_object
        else:
            raise NotImplemented('两个态矢没有统一的数据属性')


    # %%  BLOCK：重载减法运算符
    def __sub__(self, other):
        assert isinstance(other, State), '只能对算符对象做加法'
        assert self.check() and other.check(), '算符必须已经初始化'
        ##  实现队列相减
        if self.stack is not None and other.stack is not None:
            stack_temp=other.stack.copy()
            for i in range(len(stack_temp)):
                stack_temp[i]=-stack_temp[i]
            stack = self.stack + stack_temp
        else:
            stack = None

        ##  实现MPS之间的减法
        if self.mps is not None and other.mps is not None:
            mps = self.mps.add(other.mps,1,-1)
        else:
            mps = None

        ##  实现矩阵减法
        if self.vector is not None and other.vector is not None:
            vector = self.vector - other.vector
        else:
            vector = None

        ##  构造并返回结果对象
        new_object=State()
        new_object.initial_force(stack,vector,mps)
        if new_object.check():
            return new_object
        else:
            raise NotImplemented('两个态矢没有统一的数据属性')


    # %%  BLOCK：重载数乘运算符
    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float) or isinstance(other, complex)
        assert self.check() and other.check(), '算符必须已经初始化'
        ##  实现队列数乘
        if self.stack is not None:
            stack = self.stack.copy()
            for i in range(len(stack)):
                stack[i]=-stack[i]
        else:
            stack = None

        ##  实现MPS的数乘
        if self.mps is not None:
            mps=self.mps.add(self.mps,other,0)
        else:
            mps = None

        ##  实现vector数乘
        if self.vector is not None:
            vector = self.vector*other
        else:
            vector = None

        ##  构造并返回结果对象
        new_object=State()
        new_object.initial_force(stack,vector,mps)
        return new_object


    # %%  BLOCK：重载数乘运算符
    def __rmul__(self, other):
        return self.__mul__(other)


    # %%  BLOCK：计算态矢间的overlap
    def overlap(self,other):
        if self.vector is not None and other.cell_vector is not None:
            return vector_overlap(self.vector,other.cell_vector)
        elif self.mps is not None and other.mps is not None:
            return mps_overlap(self.mps,other.mps)
        elif self.stack is not None and other.stack is not None:
            self.validate(None,'vector')
            other.validate(None,'vector')
            return self.overlap(other)


    # %%  BLOCK：计算态矢在可观测量下的期望
    """
    term2qobj：计算作用量的qutip形式算符
    input.model_origin：ModelFormat对象，算符所在的模型
    input.term：TermsFormat对象或TermFormat对象
    output：float对象，期望值
    influence：本函数不改变参数对象
    """
    def expectation(self,model_origin,term,*args):
        assert isinstance(term, TermFormat) or isinstance(term, TermsFormat), '参数term必须是TermFormat或TermsFormat对象'
        assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
        model = model_preparer(model_origin, 'qutip')

        ##  判断是否初始化
        if self.check():

            ##  默认计算方式
            if len(args)==0:
                ##  优先用vector计算
                if self.vector is not None:
                    return vector_expectation(model,self.vector,term)

                ##  其次用MPS计算
                elif self.mps is not None:
                    return mps_expectation(model,self.mps,term)

                ##  最后对自身有效化
                elif self.stack is not None:
                    self.validate(model, 'vector')
                    return self.expectation(model, term)

                ##  不存在错误
                else:
                    pass

            ##  指定计算方式
            elif len(args)==1:
                if args[0] == 'vector':
                    self.validate(model, 'vector')
                    return self.expectation(model, term)
                elif args[0] == 'mps':
                    self.validate(model, 'mps')
                    return self.expectation(model, term)

        ##  抛出错误
        else:
            raise ValueError('态矢未被初始化')


    # %%  BLOCK：计算态矢作用后的结果
    """
    term2qobj：计算作用量的qutip形式算符
    input.model_origin：ModelFormat对象，算符所在的模型
    input.term：TermsFormat对象或TermFormat对象
    output：State对象，作用后的态矢
    influence：本函数不改变参数对象
    """
    def apply(self, model_origin, term, normalize,*args):
        ##  标准化
        assert isinstance(term, TermFormat) or isinstance(term, TermsFormat), '参数term必须是TermFormat或TermsFormat对象'
        assert isinstance(model_origin, ModelFormat), '参数model_origin必须是ModelFormat对象'
        model = model_preparer(model_origin, 'qutip')

        ##  初始化
        stack=None
        vector=None
        mps=None

        ##  检查态矢是否初始化
        if self.check():

            ##  不指定类型
            if len(args)==0:
                if self.vector is not None:
                    vector=vector_apply(model,self.vector,term,normalize)
                if self.mps is not None:
                    mps=mps_apply(model,self.mps,term,normalize)
                if self.stack is not None:
                    if vector is None:
                        self.validate(model,'vector')
                        vector = vector_apply(model, self.vector, term, normalize)
                    if mps is None:
                        self.validate(model,'mps')
                        mps = mps_apply(model, self.mps, term, normalize)

            ##  指定作用类型
            elif len(args)==1:

                ##  vector类型
                if args[0]=='vector':
                    self.validate(model,'vector')
                    vector = vector_apply(model, self.vector, term, normalize)

                ##  MPS类型
                elif args[0]=='mps':
                    self.validate(model,'mps')
                    mps = mps_apply(model, self.mps, term, normalize)

                ##  未实现错误
                else:
                    raise NotImplemented

        ##  抛出错误
        else:
            raise ValueError('态矢未被初始化')
        state=State()
        state.initial_force(stack, vector, mps)


    # %%  BLOCK：复制函数
    def copy(self):
        return copy.deepcopy(self)