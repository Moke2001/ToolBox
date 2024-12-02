from TenpyToolBox.Package.Term.Term import Term


class CouplingTerm(Term):
    def __init__(self, label, position_0,position_1, op_0,op_1, *args):
        super().__init__(label, *args)
        self.position_0 = position_0
        self.position_1 = position_1
        self.op_0 = op_0
        self.op_1 = op_1

    def fit(self, label,*args):
        if super().__eq__(label):
            if self.position_0 == args[0] and self.position_1 == args[1]:
                return True
        return False

    def get_op(self):
        return self.op_0, self.op_1

    def get_position(self):
        return self.position_0,self.position_1

    def change(self, op_0,op_1, *args):
        super().change(*args)
        self.op_0 = op_0
        self.op_1 = op_1

    def copy(self):
        if self.time:
            return CouplingTerm(self.label,self.position_0,self.position_1,self.op_0,self.op_1,self.function,self.function_params)
        else:
            return CouplingTerm(self.label,self.position_0,self.position_1,self.op_0,self.op_1,self.strength)