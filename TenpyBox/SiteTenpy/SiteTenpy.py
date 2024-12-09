from tenpy import Site, SpinHalfSite
from tenpy.linalg import np_conserved
from Format.SiteFormat.SiteFormat import SiteFormat
from Format.SiteFormat.SpinHalfSiteFormat import SpinHalfSiteFormat


class SiteTenpy(SiteFormat):
    def __init__(self,site_format):
        SiteFormat.__init__(self,site_format.get_dimension(),site_format.conserve)
        self.site =None
        self.operator_dict=site_format.operator_dict.copy()
        if isinstance(site_format,SpinHalfSiteFormat):
            self.site=SpinHalfSite(conserve=site_format.conserve)
        elif isinstance(site_format,SiteTenpy):
            self.site=site_format.site
        else:
            raise TypeError

    def build_site(self):
        for key in self.get_operator_dict().keys():
            if not self.site.valid_opname(key):
                self.site.add_op(key, self.get_operator_dict()[key])
            else:
                self.site.remove_op(key)
                self.site.add_op(key, self.get_operator_dict()[key])
    def get_site(self):
        self.build_site()
        return self.site