from tenpy import Lattice
from tenpy.models import CouplingMPOModel
from TenpyToolBox.Package.Term.CouplingTerm import CouplingTerm
from TenpyToolBox.Package.Term.MultiTerm import MultiTerm
from TenpyToolBox.Package.Term.OnsiteTerm import OnsiteTerm
from TenpyToolBox.Package.Term.OverallCouplingTerm import OverallCouplingTerm
from TenpyToolBox.Package.Term.OverallMultiTerm import OverallMultiTerm
from TenpyToolBox.Package.Term.OverallOnsiteTerm import OverallOnsiteTerm
from TenpyToolBox.Package.Terms.Terms import Terms


class ModelCreator(CouplingMPOModel):
    #%%  BLOCK：构造模型的作用量
    def init_terms(self, model_params):
        ##  参数获取
        term_list=model_params.get('term_list',None)
        lattice=model_params.get('lattice',None)
        time=model_params.get('time',None)
        assert isinstance(term_list,Terms),'term_list must be of type TermList'
        assert isinstance(lattice,Lattice),'lattice must be of type Lattice'

        ##  执行作用量添加
        for i in range(term_list.number):
            term_temp=term_list.get_term(i)  # 获取当前作用量

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


    #%%  BLOCK：从模型参数中获取晶格对象
    def init_lattice(self, model_params):
        return model_params.get('lattice',None)