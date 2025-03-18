import numpy as np
from Physics.QuantumComputation.CliffordSimulator.Circuit.MajoranaCircuit.MajoranaCommand import MajoranaCommand
from Physics.QuantumComputation.CliffordSimulator.Circuit.MajoranaCircuit.MajoranaFeedback import MajoranaFeedback
from Physics.QuantumComputation.CliffordSimulator.Computer.CliffordMajoranaComputer import CliffordMajoranaComputer


class MajoranaCircuit:
    #%%  USER：构造函数
    """""
    self.initialize：int对象，初始化参数
    self.measure_recorder：dict对象，记录测量结果
    self.command_vector：np.array of MajoranaCommand or MajoranaFeedback对象，指令序列
    self.command_number：int对象，指令数目
    """""
    def __init__(self):
        self.initialize=None
        self.measure_recorder=dict()
        self.command_vector=np.empty(100, dtype=MajoranaCommand or MajoranaFeedback)
        self.command_number=0


    #%%  USER：推送定义函数
    """""
    input.command：MajoranaCommand or MajoranaFeedback对象，待执行的指令
    influence：在self.command_vector添加指令，self.command_number增加一个
    """""
    def push(self,command):
        if self.command_number<self.command_vector.shape[0]:
            self.command_vector[self.command_number]=command
            self.command_number+=1
        else:
            self.command_vector=np.append(self.command_vector,np.empty(100, dtype=MajoranaCommand or MajoranaFeedback))
            self.command_vector[self.command_number]=command
            self.command_number+=1


    #%%  USER：合并两个指令序列
    """""
    input.other：MajoranaCircuit对象，待合并的线路
    influence：在self.command_vector中添加other.command_vector
    """""
    def merge(self,other):
        assert isinstance(other, MajoranaCircuit)
        self.push(other.command_vector)


    #%%  USER：第二定义函数
    """""
    input.params：list or np.array of int对象，初始化参数
    influence：修改self.initialize为params
    """""
    def initialize(self,params):
        self.initialize=params


    #%%  USER：模拟执行
    """""
    input.pauli_computer：CliffordPauliComputer对象，执行线路的量子计算机
    influence：依次执行量子指令，修改input.pauli_computer.psi，包含量子噪声
    """""
    def simulate_noise(self, majorana_computer):
        assert isinstance(majorana_computer, CliffordMajoranaComputer)
        if majorana_computer.psi is None:
            majorana_computer.initialize(self.initialize)
        for i in range(self.command_number):
            if isinstance(self.command_vector[i],MajoranaCommand):
                name=self.command_vector[i].name
                index=self.command_vector[i].index
                index_control = self.command_vector[i].control_index
                index_target = self.command_vector[i].target_index
                if name=='S':
                    majorana_computer.S(index)
                    majorana_computer.noise(index)
                elif name=='B':
                    majorana_computer.B(index_control,index_target)
                    majorana_computer.noise(index_control,index_target)
                elif name=='CZ':
                    majorana_computer.CZ(index_control, index_target)
                    majorana_computer.noise(index_control, index_target)
                elif name=='M':
                    measurement=majorana_computer.measure(index)
                    majorana_computer.noise(index)
                    if np.random.rand() < majorana_computer.probability:
                        measurement=-measurement
                    if self.command_vector[i].stamp is not None:
                        self.measure_recorder[self.command_vector[i].stamp]=measurement
            elif isinstance(self.command_vector[i],MajoranaFeedback):
                measurement_vector=np.empty(self.command_vector[i].stamp_vector.shape[0],dtype=int)
                for j in range(measurement_vector.shape[0]):
                    measurement_vector[j]=self.measure_recorder[self.command_vector[i].stamp_vector[j]]
                circuit_temp=MajoranaCircuit()
                circuit_temp.push(self.command_vector[i].decoder(measurement_vector))
                circuit_temp.simulate_noise(majorana_computer)


    #%%  USER：模拟执行
    """""
    input.pauli_computer：CliffordPauliComputer对象，执行线路的量子计算机
    influence：依次执行量子指令，修改input.pauli_computer.psi，包含量子噪声
    """""
    def simulate_quiet(self, majorana_computer):
        assert isinstance(majorana_computer, CliffordMajoranaComputer)
        if majorana_computer.psi is None:
            majorana_computer.initialize(self.initialize)
        for i in range(self.command_number):
            if isinstance(self.command_vector[i],MajoranaCommand):
                name=self.command_vector[i].name
                index=self.command_vector[i].index
                index_control = self.command_vector[i].control_index
                index_target = self.command_vector[i].target_index
                if name=='S':
                    majorana_computer.S(index)
                elif name=='B':
                    majorana_computer.B(index_control,index_target)
                elif name=='CZ':
                    majorana_computer.CZ(index_control, index_target)
                elif name=='M':
                    measurement=majorana_computer.measure(index)
                    if self.command_vector[i].stamp is not None:
                        self.measure_recorder[self.command_vector[i].stamp]=measurement
            elif isinstance(self.command_vector[i],MajoranaFeedback):
                measurement_vector=np.empty(self.command_vector[i].stamp_vector.shape[0],dtype=int)
                for j in range(measurement_vector.shape[0]):
                    measurement_vector[j]=self.measure_recorder[self.command_vector[i].stamp_vector[j]]
                circuit_temp=MajoranaCircuit()
                circuit_temp.push(self.command_vector[i].decoder(measurement_vector))
                circuit_temp.simulate_quiet(majorana_computer)