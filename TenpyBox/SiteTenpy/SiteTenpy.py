from tenpy import Site

from Format.SiteFormat.SiteFormat import SiteFormat


class SiteTenpy(SiteFormat,Site):
    def __init__(self,dimension):
        SiteFormat.__init__(self,dimension)
        pass

    def build(self):
        for key in self.get_operator_dict().keys():
            self.add_op(key, self.get_operator_dict()[key])