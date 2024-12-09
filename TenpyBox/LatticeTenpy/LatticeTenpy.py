from tenpy import Lattice
from TenpyBox.SiteTenpy.SiteTenpy import SiteTenpy
from Format.LatticeFormat.LatticeFormat import LatticeFormat


class LatticeTenpy(LatticeFormat):
    # %%  BLOCK：构造函数
    """""
    self.cell_period_list：格式类属性，元胞延展次数，形如[1,2,3]
    self.cell_vector_list：格式类属性，每个方向上的元胞基矢，形如[np.array,np.array]
    self.inner_site_list：格式类属性，元胞内Site对象列表，形如[Site,Site]
    self.inner_coordinate：格式类属性，元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：格式类属性，元胞个数
    self.space_dimension：格式类属性，空间维度数目
    self.site_number_in_one_cell：格式类属性，元胞中格点个数
    self.lattice：数据类属性，tenpy的晶格对象
    """""
    def __init__(self,lattice_format):
        super().__init__()
        cell_period_list = lattice_format.cell_period_list
        cell_vector_list = lattice_format.cell_vector_list
        inner_site_list = lattice_format.inner_site_list
        inner_coordinate_list = lattice_format.inner_coordinate_list
        super().update_lattice(cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)
        self.lattice = None


    # %%  BLOCK：构造数据类属性
    def build_lattice(self):
        site_real_list=[]
        for i in range(self.get_site_number_in_one_cell()):
            self.inner_site_list[i]=SiteTenpy(self.inner_site_list[i])
        for i in range(self.get_site_number_in_one_cell()):
            self.inner_site_list[i].build_site()
            temp=(self.inner_site_list[i])
            assert isinstance(temp,SiteTenpy)
            site_real_list.append(temp.get_site())
        self.lattice = Lattice(self.cell_period_list, site_real_list, basis=self.cell_vector_list, positions=self.inner_coordinate_list)


    # %%  BLOCK：返回位点上的Site对象
    def get_site(self, index_tuple):
        return self.lattice.get_site(index_tuple)


    # %%  BLOCK：返回数据类对象tenpy晶格对象
    def get_lattice(self):
        self.build_lattice()
        return self.lattice