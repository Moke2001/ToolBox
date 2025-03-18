

class PauliFeedback:
    #%%  USER：构造函数
    """""
    self.decoder：function对象，解码器
    self.stamp_vector：np.array of object对象，控制测量的时间戳
    """""
    def __init__(self):
        self.decoder=None
        self.stamp_vector=None
        self.command_vector=None


    #%%  USER：定义函数
    """""
    input.decoder：function对象，解码器
    input.stamp_vector：np.array of object对象，控制测量的时间戳
    """""
    def define(self,stamp_vector,decoder):
        self.decoder=decoder
        self.stamp_vector=stamp_vector
