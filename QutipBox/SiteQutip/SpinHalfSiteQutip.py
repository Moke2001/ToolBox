from Format.SiteFormat.SiteFormat import SiteFormat
from qutip import *
from Format.SiteFormat.SpinHalfSiteFormat import SpinHalfSiteFormat


class SpinHalfSiteQutip(SpinHalfSiteFormat):
    def __init__(self):
        super().__init__()
        self.op_dict=self.operator_dict.copy()


    def build(self):
        for key in self.get_operator_dict():
            self.op_dict[key]=Qobj(self.get_operator_dict()[key])
