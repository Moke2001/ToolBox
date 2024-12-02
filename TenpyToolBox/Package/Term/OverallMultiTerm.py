from TenpyToolBox.Package.Term.Term import Term




class OverallMultiTerm(Term):
    def __init__(self, label,cell_index_list,vector_list,op_list, *args):
        super().__init__(label, *args)
        self.cell_index_list=cell_index_list
        self.vector_list=vector_list
        self.op_list=op_list

    def fit(self, label,*args):
        if super().fit(label):
            if self.cell_index_list==args[0] and self.vector_list==args[1]:
                return True
        return False

    def get_op(self):
        return self.op_list

    def get_unit(self):
        return self.cell_index_list,self.vector_list

    def change(self,op_list, *args):
        super().change(*args)
        self.op_list = op_list

    def copy(self):
        if self.time:
            return OverallMultiTerm(self.label, self.cell_index_list,self.vector_list,self.op_list, self.function, self.function_params)
        else:
            return OverallMultiTerm(self.label, self.cell_index_list,self.vector_list,self.op_list, self.function, self.strength)