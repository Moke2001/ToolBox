from abc import abstractmethod
from Format.LatticeFormat.LatticeFormat import LatticeFormat
from Format.TermFormat.TermsFormat import TermsFormat


class ModelFormat(LatticeFormat,TermsFormat):
    def __init__(self):
        LatticeFormat.__init__(self)
        TermsFormat.__init__(self)


    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def get_model(self):
        pass
