from abc import abstractmethod
import numpy as np


class LatticeFormat:
    # %%  BLOCK：构造函数
    """""
    self.cell_period_list：元胞延展次数，形如[1,2,3]
    self.cell_vector_list：每个方向上的元胞基矢，形如[np.array,np.array]
    self.inner_site_list：元胞内Site对象列表，形如[Site,Site]
    self.inner_coordiante：元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：元胞个数
    self.space_dimension：空间维度数目
    self.site_number_in_one_cell：元胞中格点个数
    """""
    def __init__(self):
        ##  参数赋值
        self.cell_period_list = None  # 元胞在各个方向上的延展次数
        self.cell_number = None  # 元胞数量
        self.space_dimension = None  # 空间维度
        self.site_number_in_one_cell = None  # 一个元胞内的的格点数量
        self.site_number = None  # 系统格点数量
        self.cell_vector_list = None  # 晶格元胞基矢
        self.inner_site_list = None  # 晶格元胞内格点类型列表
        self.inner_coordinate_list= None  # 晶格元胞内格点相对坐标


    # %%  BLOCK：更新晶格形式
    def update_lattice(self, cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list):
        ##  判断参数合法性
        assert len(cell_period_list) == len(cell_vector_list)
        assert len(inner_site_list) == len(inner_coordinate_list)
        assert all(it.shape[0] == len(cell_vector_list) for it in cell_vector_list)
        assert all(it.shape[0] == len(cell_vector_list) for it in inner_coordinate_list)

        ##  参数赋值
        self.cell_period_list = cell_period_list  # 元胞在各个方向上的延展次数
        self.cell_number = np.prod(cell_period_list)  # 元胞数量
        self.space_dimension = len(cell_vector_list)  # 空间维度
        self.site_number_in_one_cell = len(inner_site_list)  # 一个元胞内的的格点数量
        self.site_number = self.site_number_in_one_cell * self.cell_number  # 系统格点数量
        self.cell_vector_list = cell_vector_list
        self.inner_site_list = inner_site_list
        self.inner_coordinate_list = inner_coordinate_list


    # %%  BLOCK：插入晶格形式
    def insert_lattice(self,lattice):
        assert isinstance(lattice, LatticeFormat),'参数lattice必须是LatticeFormat对象'
        cell_period_list=lattice.cell_period_list.copy()
        cell_vector_list=lattice.cell_vector_list.copy()
        inner_site_list=lattice.inner_site_list.copy()
        inner_coordinate_list=lattice.inner_coordinate_list.copy()
        self.update_lattice(cell_period_list, cell_vector_list, inner_site_list, inner_coordinate_list)


    #%%  BLOCK：构造晶格对象
    @ abstractmethod
    def build_lattice(self):
        pass


    # %%  BLOCK：获得格点坐标
    def get_position(self, cell_index_tuple,inner_index):
        result = np.zeros(self.space_dimension)
        for i in range(self.space_dimension):
            result = result + self.cell_vector_list[i] * cell_index_tuple[i]
        result = result + self.inner_coordinate_list[inner_index]
        return result


    #%%  BLOCK：获得晶格结构数组
    def get_structure(self,type):
        return np.array(tuple(self.cell_period_list+[self.site_number_in_one_cell]),dtype=type)


    #%%  BLOCK：获得总格点数目
    def get_site_number(self):
        return self.site_number


    #%%  BLOCK：返回一个元胞内格点的数目
    def get_site_number_in_one_cell(self):
        return self.site_number_in_one_cell


    # %%  BLOCK：求两个Site间的距离
    def get_distance(self, cell_index_tuple_0,inner_index_0,cell_index_tuple_1,inner_index_1):
        position_0 = self.get_position(cell_index_tuple_0,inner_index_0)
        position_1 = self.get_position(cell_index_tuple_1,inner_index_1)
        return np.linalg.norm(position_0 - position_1)


    #%%  BLOCK：返回格点对象
    @abstractmethod
    def get_site(self,index_tuple):
        pass


    #%%  BLOCK：返回晶格对象
    @abstractmethod
    def get_lattice(self):
        pass
