from TenpyToolBox.Package.Term.Term import Term


class OverallCouplingTerm(Term):
    def __init__(self, label, cell_index_0,cell_index_1,vector,op_0,op_1, *args):
        super().__init__(label, *args)
        self.cell_index_0 = cell_index_0
        self.cell_index_1 = cell_index_1
        self.vector = vector
        self.op_0 = op_0
        self.op_1 = op_1

    def fit(self, label,*args):
        if super().fit(label):
            if self.cell_index_0 == args[0] and self.cell_index_1 == args[1] and self.vector == args[2]:
                return True
        return False

    def get_op(self):
        return self.op_0,self.op_1

    def get_unit(self):
        return self.cell_index_0,self.cell_index_1,self.vector

    def change(self, op_0,op_1, *args):
        super().change(*args)
        self.op_0 = op_0
        self.op_1 = op_1

    def copy(self):
        if self.time:
            return OverallCouplingTerm(self.label, self.cell_index_0,self.cell_index_1, self.op_0,self.op_1, self.function, self.function_params)
        else:
            return OverallCouplingTerm(self.label, self.cell_index_0,self.cell_index_1, self.op_0,self.op_1, self.strength)
