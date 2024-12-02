from TenpyToolBox.Package.Term.Term import Term


class MultiTerm(Term):
    def __init__(self, label, position_list, op_list, *args):
        super().__init__(label, *args)
        self.position_list = position_list
        self.op_list = op_list

    def fit(self, label,*args):
        if super().__eq__(label):
            if self.position_list == args[0]:
                return True
        return False

    def get_op(self):
        return self.op_list

    def get_position(self):
        return self.position_list

    def change(self, op_list, *args):
        super().change(*args)
        self.op_list = op_list

    def copy(self):
        if self.time:
            return MultiTerm(self.label, self.position_list, self.op_list, self.function, self.function_params)
        else:
            return MultiTerm(self.label, self.position_list, self.op_list, self.strength)