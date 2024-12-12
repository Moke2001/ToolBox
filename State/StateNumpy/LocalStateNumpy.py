import numpy as np


class LocalStateNumpy:
    #%%  USER：构造函数
    """"
    self.dimension：int对象，局域Hilbert空间维度
    self.amount_array：np.ndarray对象，对应基矢系数
    """""
    def __init__(self,dimension:int,amount_array:np.ndarray):
        ##  标准化
        assert isinstance(dimension,int),'参数dimension必须是int对象'
        assert isinstance(amount_array,np.ndarray),'参数amount_array必须是np.ndarray对象'
        assert dimension==amount_array.shape[0],'参数dimension必须和参数amount_array维度匹配'

        ##  赋值
        self.dimension=dimension  # 局域Hilbert空间维度
        self.amount_array=amount_array  # 基矢系数


    #%%  KEY：获得系数数组
    """"
    get_amount_array：获得态矢数组表示
    output：np.ndarray对象，数组表示
    influence：本函数不改变参数对象
    """""
    def get_amount_array(self)->np.ndarray:
        return self.amount_array


    #%%  KEY：获得局域Hilbert空间维度
    """"
    get_dimension：获得局域Hilbert空间维度
    output：int对象，局域Hilbert空间维度
    influence：本函数不改变参数对象
    """""
    def get_dimension(self)->int:
        return self.dimension


    #%%  KEY：重载取值运算符
    """"
    __getitem__：取对应基矢序号的系数
    output：float or complex对象，态矢在对应基矢上的投影分量
    influence：本函数不改变参数对象
    """""
    def __getitem__(self,index)->float or complex:
        return self.amount_array[index]
