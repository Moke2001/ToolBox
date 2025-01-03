import numpy as np


class LatticeFormat:
    # %%  USER：构造函数
    """""
    LatticeFormat：格式晶格类
    self.cell_period_list：元胞延展次数，形如[1,2,3]
    self.cell_vector_list：每个方向上的元胞基矢，形如[np.array,np.array]
    self.inner_site_list：元胞内Site对象列表，形如[Site,Site]
    self.inner_coordinate：元胞内格点位移，形如[np.array,np.array]，与cell_sites对应
    self.cell_number：元胞个数
    self.space_dimension：空间维度数目
    self.site_number_in_one_cell：元胞中格点个数
    """""
    def __init__(self,*args):
        ##  SECTION：空构造函数---------------------------------------------------------------------
        if len(args) == 0:
            self.cell_period_list = None  # 元胞在各个方向上的延展次数
            self.cell_vector_list = None  # 晶格元胞基矢
            self.inner_site_list = None  # 晶格元胞内格点类型列表
            self.inner_coordinate_list= None  # 晶格元胞内格点相对坐标
            self.periodicity=False

        ##  SECTION：复制构造函数-------------------------------------------------------------------
        elif len(args) == 1 and isinstance(args[0], LatticeFormat):
            ##  基础定义量
            self.cell_period_list = args[0].get_cell_period_list().copy()  # 元胞在各个方向上的延展次数
            self.cell_vector_list = args[0].get_cell_vector_list().copy()  # 晶格元胞基矢
            self.inner_site_list = args[0].get_inner_site_list().copy()  # 晶格元胞内格点类型列表
            self.inner_coordinate_list = args[0].get_inner_coordinate_list().copy()  # 晶格元胞内格点相对坐标
            self.periodicity = args[0].get_periodicity()  # 晶格周期性

        ##  SECTION：标准构造函数-------------------------------------------------------------------
        elif len(args) == 4:
            ##  标准化
            cell_period_list=args[0]
            cell_vector_list=args[1]
            inner_site_list=args[2]
            inner_coordinate_list=args[3]
            assert len(cell_period_list) == len(cell_vector_list)
            assert len(inner_site_list) == len(inner_coordinate_list)
            assert all(it.shape[0] == len(cell_vector_list) for it in cell_vector_list)
            assert all(it.shape[0] == len(cell_vector_list) for it in inner_coordinate_list)

            ##  赋值
            self.cell_period_list = cell_period_list
            self.cell_vector_list = cell_vector_list
            self.inner_site_list = inner_site_list
            self.inner_coordinate_list = inner_coordinate_list
            self.periodicity = False

        ##  SECTION：标准构造函数2------------------------------------------------------------------
        elif len(args) == 5:
            ##  标准化
            cell_period_list=args[0]
            cell_vector_list=args[1]
            inner_site_list=args[2]
            inner_coordinate_list=args[3]
            periodicity=args[4]
            assert len(cell_period_list) == len(cell_vector_list)
            assert len(inner_site_list) == len(inner_coordinate_list)
            assert all(it.shape[0] == len(cell_vector_list) for it in cell_vector_list)
            assert all(it.shape[0] == len(cell_vector_list) for it in inner_coordinate_list)
            assert isinstance(periodicity, bool) or isinstance(periodicity,list),'参数periodicity必须是list对象'

            ##  赋值
            self.cell_period_list = cell_period_list
            self.cell_vector_list = cell_vector_list
            self.inner_site_list = inner_site_list
            self.inner_coordinate_list = inner_coordinate_list
            self.periodicity = periodicity

    # %%  USER：获得格点坐标
    """""
    input.index_tuple：格坐标
    output：格点空间坐标
    influence：本函数不改变参数对象
    """""
    def get_position(self, index_tuple):
        result = np.zeros(self.get_space_dimension())
        for i in range(self.get_space_dimension()):
            result = result + self.cell_vector_list[i] * index_tuple[i]
        result = result + self.inner_coordinate_list[index_tuple[-1]]
        return result


    # %%  USER：求两个Site间的距离
    """""
    input.index_tuple_0：前一个格坐标
    input.index_tuple_1：后一个格坐标
    output：float对象，格点距离
    influence：本函数不改变参数对象
    """""
    def get_distance(self, index_tuple_0, index_tuple_1):
        position_0 = self.get_position(index_tuple_0)
        position_1 = self.get_position(index_tuple_1)
        return np.linalg.norm(position_0 - position_1)


    #%%  KEY：返回晶格循环周期
    """
    get_cell_period_list：返回晶格循环周期
    output：list of int对象，晶格循环周期列表
    """
    def get_cell_period_list(self):
        return self.cell_period_list


    #%%  KEY：返回晶格格矢
    """
    get_cell_vector_list：返回格矢
    output：list of np.ndarray对象，格矢列表
    """
    def get_cell_vector_list(self):
        return self.cell_vector_list


    #%%  KEY：返回晶格元胞内格点列表
    """
    get_inner_site_list：返回晶格元胞内格点列表
    output：list of SiteFormat对象，晶格元胞内格点列表
    """
    def get_inner_site_list(self):
        return self.inner_site_list


    #%%  KEY：返回晶格元胞内格点列表
    """
    get_inner_coordinate_list：返回晶格元胞内格点坐标
    output：list of np.ndarray对象，晶格元胞内格点坐标
    """
    def get_inner_coordinate_list(self):
        return self.inner_coordinate_list


    #%%  KEY：获得空间维度数
    """""
    output：int对象，晶格几何空间维度
    influence：本函数不改变参数对象
    """""
    def get_space_dimension(self):
        return len(self.cell_period_list)


    #%%  KEY：获得元胞数目
    """""
    output：int对象，元胞数目
    influence：本函数不改变参数对象
    """""
    def get_cell_number(self):
        return np.prod(self.cell_period_list)


    #%%  KEY：获得总格点数目
    """""
    output：int对象，所有格点总数目
    influence：本函数不改变参数对象
    """""
    def get_site_number(self):
        return np.prod(self.cell_period_list)*len(self.inner_site_list)


    #%%  KEY：返回一个元胞内格点的数目
    """""
    output：int对象，一个元胞内格点数目
    influence：本函数不改变参数对象
    """""
    def get_site_number_in_one_cell(self):
        return len(self.inner_site_list)


    #%%  KEY：返回晶格局域维度数组
    def get_dimension_array(self):
        array=np.empty(self.cell_period_list + [len(self.inner_site_list)], dtype=int)
        for index_tuple_temp, object_temp in np.ndenumerate(array):
            array[index_tuple_temp] = self.inner_site_list[index_tuple_temp[-1]].get_dimension()
        return array


    #%%  KEY：获得Site局域算符局域numpy形式
    def get_site_operator_numpy(self, index_tuple, name):
        assert isinstance(name,str),'参数name必须是str对象'
        if isinstance(index_tuple,tuple):
            return self.inner_site_list[index_tuple[-1]].get_operator_dictionary()[name]
        elif isinstance(index_tuple,int):
            return self.inner_site_list[index_tuple].get_operator_dictionary()[name]


    #%%  KEY：获得Site局域算符字典
    def get_site_operator_dictionary(self,index_tuple):
        if isinstance(index_tuple,tuple):
            return self.inner_site_list[index_tuple[-1]].get_operator_dictionary()
        elif isinstance(index_tuple,int):
            return self.inner_site_list[index_tuple].get_operator_dictionary()


    #%%  KEY：获得Site局域维度
    def get_site_dimension(self,index_tuple):
        if isinstance(index_tuple,tuple):
            return self.inner_site_list[index_tuple[-1]].get_dimension()
        elif isinstance(index_tuple,int):
            return self.inner_site_list[index_tuple].get_dimension()


    #%%  KEY：获得周期性
    def get_periodicity(self):
        return self.periodicity