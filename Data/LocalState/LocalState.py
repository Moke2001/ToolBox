import numpy as np


class LocalState:
    #%%  BLOCK：构造函数
    """
    self.dimension：int对象，局域Hilbert空间维度
    self.amount_array：np.ndarray对象，对应基矢系数
    """
    def __init__(self,dimension:int,amount_array:np.ndarray):
        ##  标准化
        assert isinstance(dimension,int),'参数dimension必须是int对象'
        assert isinstance(amount_array,np.ndarray),'参数amount_array必须是np.ndarray对象'
        assert dimension==amount_array.shape[0],'参数dimension必须和参数amount_array维度匹配'

        ##  赋值
        self.dimension=dimension
        self.amount_array=amount_array


    #%%  BLOCK：获得系数数组
    def get_amount_array(self):
        return self.amount_array


    #%%  BLOCK：获得局域Hilbert空间维度
    def get_dimension(self):
        return self.dimension


    #%%  BLOCK：重载取值运算符
    def __getitem__(self,index):
        return self.amount_array[index]
