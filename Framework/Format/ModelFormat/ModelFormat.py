import copy
from abc import abstractmethod
from Framework.Format.LatticeFormat.LatticeFormat import LatticeFormat
from Framework.Format.TermFormat.TermsFormat import TermsFormat


class ModelFormat(LatticeFormat,TermsFormat):
    def __init__(self,*args):
        if len(args)==0:
            LatticeFormat.__init__(self)
            TermsFormat.__init__(self)
        elif len(args)==1 and isinstance(args[0],ModelFormat):
            LatticeFormat.__init__(self)
            TermsFormat.__init__(self)
            cell_period_list=args[0].cell_period_list.copy()
            cell_vector_list=args[0].cell_vector_list.copy()
            inner_site_list =args[0].inner_site_list.copy()
            inner_coordinate_list=args[0].inner_coordinate_list.copy()
            self.update_lattice(self, cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)
            terms=args[0].terms.copy()
            self.initial(terms)
        else:
            raise ValueError('参数形式错误')


    @abstractmethod
    def build(self):
        pass


    @abstractmethod
    def get_model(self):
        pass


    def copy(self):
        return copy.deepcopy(self)
