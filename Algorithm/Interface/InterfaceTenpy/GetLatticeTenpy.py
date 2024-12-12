from tenpy import Lattice, LegCharge, Site
from Format.ModelFormat.ModelFormat import ModelFormat


#%%  KEY：返回tenpy晶格对象
"""
input.model：ModelFormat对象，模型
output：Lattice对象，tenpy晶格
"""
def get_lattice_tenpy(model)->Lattice:
    ##  SECTION：标准化-----------------------------------------------------------------------------
    assert isinstance(model,ModelFormat),'参数model必须是ModelFormat对象'

    ##  SECTION：获取参数---------------------------------------------------------------------------
    cell_period_list=model.get_cell_period_list()
    cell_vector_list=model.get_cell_vector_list()
    inner_coordinate_list=model.get_inner_coordinate_list()

    ##  SECTION：获取元胞tenpy格点------------------------------------------------------------------
    site_tenpy_list=[]
    for i in range(len(model.get_inner_site_list())):

        ##  根据维度定义Site对象
        site_temp=Site(LegCharge.from_trivial(model.get_inner_site_list()[i].get_dimension()))

        ##  添加算符
        for key in model.get_inner_site_list()[i].get_operator_dictionary().keys():
            if not site_temp.valid_opname(key):
                site_temp.add_op(key, model.get_inner_site_list()[i].get_operator_dictionary()[key])
            else:
                site_temp.remove_op(key)
                site_temp.add_op(key, model.get_inner_site_list()[i].get_operator_dictionary()[key])
        site_tenpy_list.append(site_temp)

    ##  SECTION：返回结果---------------------------------------------------------------------------
    return Lattice(cell_period_list, site_tenpy_list, basis=cell_vector_list, positions=inner_coordinate_list)
