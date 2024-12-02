from TenpyToolBox.Package.Term.Term import Term


class OverallOnsiteTerm(Term):
    def __init__(self, label, cell_index,op, *args):
        super().__init__(label, *args)
        self.cell_index = cell_index
        self.op = op

    def fit(self, label,*args):
        if super().fit(label):
            if self.cell_index == args[0]:
                return True
        return False

    def get_op(self):
        return self.op

    def get_unit(self):
        return self.cell_index

    def change(self, op, *args):
        super().change(*args)
        self.op = op

    def copy(self):
        if self.time:
            return OverallOnsiteTerm(self.label, self.cell_index, self.op, self.function, self.function_params)
        else:
            return OverallOnsiteTerm(self.label, self.cell_index, self.op, self.strength)