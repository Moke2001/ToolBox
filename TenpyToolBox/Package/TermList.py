from TenpyToolBox.Package.Term import Term, OnsiteTerm, CouplingTerm, MultiTerm, OverallOnsiteTerm, OverallCouplingTerm, \
    OverallMultiTerm


class TermList:
    def __init__(self):
        self.terms = []
        self.number=0

    def get_term(self,index):
        return self.terms[index]

    def push(self, term):
        assert isinstance(term,Term),'term must be of type Term'
        self.terms.append(term)
        self.number+=1

    def pull(self,index):
        self.terms.pop(index)
        self.number-=1

    def change(self,*args):
        type=self.judeg_type(*args)
        term_index=self.find(*args)
        self.terms[term_index]=type(*args)

    def find(self,*args):
        type=self.judeg_type(*args)
        term_target=type(*args)
        for i in range(len(self.terms)):
            if self.terms[i]==term_target:
                return i
        return None

    def judeg_type(self,*args):
        ##  OnsiteTerm(label,position,op,strength/[function,function_params])
        if isinstance(args[1],tuple) and isinstance(args[2],str):
            return OnsiteTerm
        ##  CouplingTerm(label,position_0,positon_1,op_0,op_1,strength/[function,function_params])
        elif isinstance(args[1],tuple) and isinstance(args[2],tuple):
            return CouplingTerm
        ##  OverallOnsiteTerm(label,cell_index,op,strength/[function,function_params])
        elif isinstance(args[1],int) and isinstance(args[2],str):
            return OverallOnsiteTerm
        ##  OverallCouplingTerm(label,cell_index_0,cell_index_1,vector,op_0,op_1,strength/[function,function_params])
        elif isinstance(args[1],int) and isinstance(args[2],int):
            return OverallCouplingTerm
        elif isinstance(args[1],list) and isinstance(args[2],list):
            ##  OverallMultiTerm(label,cell_index_list,vector_list,op_list,strength/[function,function_params])
            if isinstance(args[1][0],tuple):
                return MultiTerm
            ##  MultiTerm(label,position_list,op_list,strength/[function,function_params])
            else:
                return OverallMultiTerm
        else:
            raise TypeError('Type is not supported')

    def clear(self):
        self.terms = []
        self.number=0