from QutipToolBox.Site.Site import Site
from qutip import *


class SpinHalfSite(Site):
    # %%  BLOCK：构造函数
    def __init__(self):
        super().__init__(2)
        self.push_operator('sigmax',sigmax())
        self.push_operator('sigmay',sigmay())
        self.push_operator('sigmaz',sigmaz())
        self.push_operator('sigmaup',0.5*(sigmax()+identity(2)))
        self.push_operator('sigmadown',0.5*(sigmax()-identity(2)))
        self.push_operator('sigmaplus',sigmap())
        self.push_operator('sigmauminus',sigmam())

