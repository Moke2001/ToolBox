from tenpy import Lattice, MPS
from tenpy.models import CouplingMPOModel
from TenpyToolBox.ModelPackage.ModelCreator import ModelCreator
from Framework.Term.Terms import Terms


class ModelPackage(Terms):
    #%%  BLOCK：ModelPackage构造函数
    def __init__(self):
        super().__init__()
        self.model=None
        self.lattice=None


    #%%  BLOCK：建构模型，将ModelPackage的参数加载给Model对象
    def build(self):
        if self.lattice is not None:
            model_params = {
                'term_list': self,
                'lattice': self.lattice,
                'time': 0,
            }
        else:
            raise ValueError('Lattice not built')
        self.model=ModelCreator(model_params)


    #%%  BLOCK：返回Model对象
    def get_model(self) -> CouplingMPOModel:
        self.build()
        return self.model


    #%%  BLOCK：定义模型的Lattice对象
    def update_lattice(self,lattice:Lattice):
        self.lattice=lattice


    #%%  BLOCK：返回Lattice对象
    def get_lattice(self) -> Lattice:
        return self.lattice


    #%%  BLOCK：返回模型的格点数目
    def get_site_number(self)->int:
        return len(self.get_sites())


    #%%  BLOCK：返回按照MPS顺序排列的Site对象列表
    def get_sites(self):
        return self.lattice.mps_sites()


    #%%  BLOCK：返回一个MPS序号对应的格点的格坐标
    def position2mps_index(self,mps_index):
        return self.lattice.mps2lat_idx(mps_index)


    #%%  BLOCK：返回一个格点格坐标对应的MPS序号
    def mps_index2position(self,position):
        return self.lattice.lat2mps_idx(position)


    #%%  BLOCK：返回模型的哈密顿量
    def get_hamiltonian(self):
        self.build()
        return self.model.calc_H_MPO()


    #%%  BLOCK：按照要求生成模型对应的态矢
    def state_creator(self,type,*args):
        if type=='product':
            states=args[0]
            return MPS.from_product_state(self.get_sites(),states)
        elif type=='random':
            chi=args[0]
            return MPS.from_random_unitary_evolution(self.get_sites(),chi,[0]*self.get_site_number())
        else:
            raise NotImplementedError

