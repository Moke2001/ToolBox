from Format.SiteFormat.SiteFormat import SiteFormat
from qutip import *

class SiteQutip(SiteFormat):
    def __init__(self,dimension):
        super().__init__(dimension)
        self.op_dict=self.operator_dict.copy()


    def build(self):
        for key in self.get_operator_dict():
            self.op_dict[key]=Qobj(self.get_operator_dict()[key])
