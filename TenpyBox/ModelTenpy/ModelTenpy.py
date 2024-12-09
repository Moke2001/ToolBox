from Format.ModelFormat.ModelFormat import ModelFormat
from TenpyBox.LatticeTenpy.LatticeTenpy import LatticeTenpy
from TenpyBox.ModelTenpy.ModelCreator import ModelCreator


class ModelTenpy(ModelFormat,LatticeTenpy):
    def __init__(self):
        ModelFormat.__init__(self)
        LatticeTenpy.__init__(self)
        self.model=None
        self.lindbladian_list=None
        self.noise_list=None


    def build(self):
        LatticeTenpy.build(self)
        model_params = {
            'term_list': self,
            'lattice': self.get_lattice(),
            'time': 0,
        }
        self.model=ModelCreator(model_params)
        for i in range(len(self.terms)):
            if self.terms[i].effect=='noise':
                self.noise_list[i]=self.noise_list[i]
            elif self.terms[i].effect=='lindbladian':
                self.lindbladian_list[i]=self.lindbladian_list[i]
            else:
                raise TypeError


    def get_model(self):
        self.build()
        return self.model
