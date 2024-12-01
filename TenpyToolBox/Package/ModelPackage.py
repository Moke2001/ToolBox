##  ModelPackage类：将Tenpy中的模型打包，方便使用，定义了量子系统的哈密顿量和Hilbert空间
from tenpy import Lattice, MPS
from tenpy.models import CouplingMPOModel
from TenpyToolBox.Package.Term import OnsiteTerm, CouplingTerm, MultiTerm, OverallMultiTerm, OverallOnsiteTerm, OverallCouplingTerm
from TenpyToolBox.Package.TermList import TermList


class ModelPackage(TermList):
    ##  构造函数，生成空模型
    def __init__(self):
        super().__init__()
        self.model=None
        self.lattice=None

    ##  建构模型，将ModelPackage的参数加载给Model类
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

    ##  返回Model类对象
    def get_model(self) -> CouplingMPOModel:
        self.build()
        return self.model

    ##  定义模型的Lattice对象
    def update_lattice(self,lattice:Lattice):
        self.lattice=lattice

    ##  返回Lattice对象
    def get_lattice(self) -> Lattice:
        return self.lattice

    ##  返回模型的格点数目
    def get_site_number(self)->int:
        return len(self.get_sites())

    ##  返回按照MPS顺序排列的Site对象列表
    def get_sites(self):
        return self.lattice.mps_sites()

    ##  返回一个MPS序号对应的格点的格坐标
    def get_position(self,mps_index):
        return self.lattice.mps2lat_idx(mps_index)

    ##  返回一个格点格坐标对应的MPS序号
    def get_mps_index(self,position):
        return self.lattice.lat2mps_idx(position)

    ##  返回模型的哈密顿量
    def get_hamiltonian(self):
        self.build()
        return self.model.calc_H_MPO()

    ##  按照要求生成模型对应的态矢
    def state_creator(self,type,*args):
        if type=='product':
            states=args[0]
            return MPS.from_product_state(self.get_sites(),states)
        elif type=='random':
            chi=args[0]
            return MPS.from_random_unitary_evolution(self.get_sites(),chi,[0]*self.get_site_number())
        else:
            raise NotImplementedError


##  构造ModelPackage指定的Model对象
class ModelCreator(CouplingMPOModel):
    ##  构造模型的作用量
    def init_terms(self, model_params):
        ##  参数获取
        term_list=model_params.get('term_list',None)
        lattice=model_params.get('lattice',None)
        time=model_params.get('time',None)
        assert isinstance(term_list,TermList),'term_list must be of type TermList'
        assert isinstance(lattice,Lattice),'lattice must be of type Lattice'

        ##  执行作用量添加
        for i in range(term_list.number):
            term_temp=term_list.get_term(i)

            ##  单局域作用量
            if isinstance(term_temp,OnsiteTerm):
                mps_index=lattice.lat2mps_idx(term_temp.get_position())
                if term_temp.time:
                    strength=term_temp.function(time,term_temp.function_params)
                else:
                    strength=term_temp.strength
                self.add_onsite_term(strength,mps_index,term_temp.get_op())

            ##  单两体相互作用量
            elif isinstance(term_temp,CouplingTerm):
                position_0,position_1=term_temp.get_position()
                mps_index_0=lattice.lat2mps_idx(position_0)
                mps_index_1=lattice.lat2mps_idx(position_1)
                op_0,op_1=term_temp.get_op()
                if term_temp.time:
                    strength=term_temp.function(time,term_temp.function_params)
                else:
                    strength=term_temp.strength
                self.add_coupling_term(strength,mps_index_0,mps_index_1,op_0,op_1)

            ##  单多体相互作用量
            elif isinstance(term_temp,MultiTerm):
                op_list=term_temp.get_op()
                position_list=term_temp.get_position()
                mps_index_list=[lattice.lat2mps_idx(position)**2 for position in position_list]
                if term_temp.time:
                    strength=term_temp.function(time,term_temp.function_params)
                else:
                    strength=term_temp.strength
                self.add_multi_coupling_term(strength,mps_index_list,op_list,['Id']*(len(position_list)-1))

            ##  遍历局域相互作用量
            elif isinstance(term_temp,OverallOnsiteTerm):
                cell_index=term_temp.get_unit()
                op=term_temp.get_op()
                if term_temp.time:
                    strength=term_temp.function(time,term_temp.function_params)
                else:
                    strength=term_temp.strength
                self.add_onsite(strength,cell_index, op, category=None, plus_hc=False)

            ##  遍历两体相互作用量
            elif isinstance(term_temp,OverallCouplingTerm):
                cell_index_0,cell_index_1,vector=term_temp.get_unit()
                op_0,op_1=term_temp.get_op()
                if term_temp.time:
                    strength=term_temp.function(time,term_temp.function_params)
                else:
                    strength=term_temp.strength
                self.add_coupling(strength, cell_index_0, op_0, cell_index_1, op_1, vector)

            ##  遍历多体相互作用量
            elif isinstance(term_temp,OverallMultiTerm):
                cell_list,vector_list=term_temp.get_unit()
                op_list=term_temp.get_op()
                if term_temp.time:
                    strength=term_temp.function(time,term_temp.function_params)
                else:
                    strength=term_temp.strength
                unit_list=[]
                for i in range(len(cell_list)):
                    unit_list.append((op_list[i],vector_list[i],cell_list[i]))
                self.add_multi_coupling(strength, unit_list, op_list)

            ##  抛出类型错误
            else:
                raise TypeError('Unexpected term type')

    ##  从模型参数中获取晶格对象
    def init_lattice(self, model_params):
        return model_params.get('lattice',None)