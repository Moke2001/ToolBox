import numpy as np
from tenpy import SpinHalfSite

from Format.SiteFormat.SpinHalfSiteFormat import SpinHalfSiteFormat


class SpinHalfSiteTenpy(SpinHalfSiteFormat,SpinHalfSite):
    def __init__(self,conserve):
        SpinHalfSite.__init__(self,conserve=conserve)
        SpinHalfSiteFormat.__init__(self)

    def build(self):
        for key in self.get_operator_dict().keys():
            self.add_op(key,self.get_operator_dict()[key])