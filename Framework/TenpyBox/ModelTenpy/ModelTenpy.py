from tenpy.models import CouplingMPOModel

from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.TenpyBox.LatticeTenpy.LatticeTenpy import LatticeTenpy
from Framework.TenpyBox.ModelTenpy.ModelCreator import ModelCreator


class ModelTenpy(ModelFormat,LatticeTenpy):
    # %%  BLOCK：构造函数
    """""
    Qutip数据类：模型对象，定义哈密顿量，多重继承
    self.model：数据类属性，tenpy模型对象
    self.lindbladian_list：数据类属性，lindblad算符对象列表
    self.noise_list：数据类属性，作用量形式列表的噪声算符列表
    self.lattice：数据类对象，tenpy晶格对象
    self.terms：格式类属性，list of Term对象，储存模型的作用量
    self.number：格式类属性，int对象，储存作用量个数
    self.cell_period_list：格式类属性，元胞延展次数，形如[1,2,3]
    self.cell_vector_list：格式类属性，每个方向上的元胞基矢，形如[np.array,np.array]
    self.inner_site_list：格式类属性，元胞内Site对象列表，形如[Site,Site]
    self.inner_coordiante：格式类属性，元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：格式类属性，元胞个数
    self.space_dimension：格式类属性，空间维度数目
    self.site_number_in_one_cell：格式类属性，元胞中格点个数
    """""
    def __init__(self,model_format):
        ModelFormat.__init__(self)
        LatticeTenpy.__init__(self,model_format)
        self.terms = model_format.terms.copy()
        self.number = model_format.number
        self.model=None
        self.lindbladian_list=[]
        self.noise_list=[]


    def initial_check(self):
        if self.model is not None and self.lindbladian_list!=[] and self.noise_list!=[]:
            return True
        else:
            return False


    #%%  BLOCK：构造数据类属性
    def build(self):
        LatticeTenpy.build_lattice(self)
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
            elif self.terms[i].effect=='hamiltonian':
                pass
            else:
                raise TypeError


    #%%  BLOCK：返回tenpy模型对象
    def get_model(self)->CouplingMPOModel:
        self.build()
        return self.model
