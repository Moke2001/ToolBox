class Term:
    def __init__(self, label,*args):
        self.label = label
        if len(args)==1:
            self.time=False
            self.strength=args[0]
        elif len(args)==2:
            self.time=True
            self.function=args[0]
            self.function_params=args[1]
        else:
            raise ValueError("Wrong number of arguments")

    def __eq__(self, other):
        assert isinstance(other, Term),'Term must be of type Term'
        return self.label == other.label

    def get_label(self):
        return self.label

    def change(self,*args):
        if len(args)==1:
            self.time=False
            self.strength=args[0]
        elif len(args)==2:
            self.time=True
            self.function=args[0]
            self.function_params=args[1]
        else:
            raise ValueError("Wrong number of arguments")


class OnsiteTerm(Term):
    def __init__(self,label,position,op,*args):
        super().__init__(label,*args)
        self.position = position
        self.op = op

    def __eq__(self,other):
        if super().__eq__(other):
            if self.position==other.mps_index:
                return True
        return False

    def get_op(self):
        return self.op

    def get_position(self):
        return self.position

    def change(self,op,*args):
        self.op=op
        super().change(*args)

    def copy(self):
        if self.time:
            return OnsiteTerm(self.label,self.position,self.op,self.function,self.function_params)
        else:
            return OnsiteTerm(self.label,self.position,self.op,self.strength)

class CouplingTerm(Term):
    def __init__(self, label, position_0,position_1, op_0,op_1, *args):
        super().__init__(label, *args)
        self.position_0 = position_0
        self.position_1 = position_1
        self.op_0 = op_0
        self.op_1 = op_1

    def __eq__(self, other):
        if super().__eq__(other):
            if self.position_0 == other.position_0 and self.position_1 == other.position_1:
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


class MultiTerm(Term):
    def __init__(self, label, position_list, op_list, *args):
        super().__init__(label, *args)
        self.position_list = position_list
        self.op_list = op_list

    def __eq__(self, other):
        if super().__eq__(other):
            if self.position_list == other.position_list:
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

class OverallOnsiteTerm(Term):
    def __init__(self, label, cell_index,op, *args):
        super().__init__(label, *args)
        self.cell_index = cell_index
        self.op = op

    def __eq__(self, other):
        if super().__eq__(other):
            if self.cell_index == other.cell_index:
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
            return MultiTerm(self.label, self.cell_index, self.op, self.function, self.function_params)
        else:
            return MultiTerm(self.label, self.cell_index, self.op, self.strength)

class OverallCouplingTerm(Term):
    def __init__(self, label, cell_index_0,cell_index_1,vector,op_0,op_1, *args):
        super().__init__(label, *args)
        self.cell_index_0 = cell_index_0
        self.cell_index_1 = cell_index_1
        self.vector = vector
        self.op_0 = op_0
        self.op_1 = op_1

    def __eq__(self, other):
        if super().__eq__(other):
            if self.cell_index_0 == other.cell_index_0 and self.cell_index_1 == other.cell_index_1 and self.vector == other.vector:
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
            return MultiTerm(self.label, self.cell_index_0,self.cell_index_1, self.op_0,self.op_1, self.function, self.function_params)
        else:
            return MultiTerm(self.label, self.cell_index_0,self.cell_index_1, self.op_0,self.op_1, self.strength)


class OverallMultiTerm(Term):
    def __init__(self, label,cell_index_list,vector_list,op_list, *args):
        super().__init__(label, *args)
        self.cell_index_list=cell_index_list
        self.vector_list=vector_list
        self.op_list=op_list

    def __eq__(self, other):
        if super().__eq__(other):
            if self.cell_index_list==other.cell_index_list and self.vector_list==other.vector_list:
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