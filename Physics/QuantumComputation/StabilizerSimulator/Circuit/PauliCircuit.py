import numpy as np


class PauliCircuit:
    def __init__(self,pauli_code):
        self.pauli_code=pauli_code
        self.computer=self.pauli_code.computer


    # %%  USER：逻辑操作指令
    def logical_X(self,index):
        pass


    # %%  USER：
    def logical_Z(self,index):
        pass

    
    #%%  USER：纠错操作指令
    def correct(self):
        pass


    # %%  USER：征状测量指令
    def extract(self):
        pass


    # %%  USER：解码器
    def decoder(self, syndrome_list):
        pass


    # %%  USER：计算错误率
    def get_error_ratio(self, sample_number,cycle_number):
        error_ratio_list=[]
        for p in np.arange(0, 0.5, 0.01):
            self.computer.set_p(p)
            correct_number=0
            for i in range(len(sample_number)):
                self.computer.initialize(0)
                psi_target=self.computer.psi.copy()
                for j in range(cycle_number):
                    self.logical_X(np.random.randint(0,self.computer.N))
                    self.extract()
                    self.correct()
                    self.logical_Z(np.random.randint(0,self.computer.N))
                    self.extract()
                    self.correct()
                if self.computer.psi==psi_target:
                    correct_number+=1
            error_ratio_list.append( (sample_number-correct_number)/sample_number)
        return error_ratio_list