import numpy as np
from Algebra.Group.MajoranaGroup import MajoranaGroup


class CliffordMajoranaComputer:
    #%%  USER：构造函数
    """""
    self.number_site：int对象，sites数目
    self.probability：float对象，错误发生几率
    self.psi：np.array of MajoranaGroup对象，态矢的稳定子生成元数组
    """""
    def __init__(self):
        self.number_site = None
        self.probability = None
        self.psi = None


    #%%  USER：定义函数
    """""
    input.number_site：int对象，sites数目
    input.probability：float对象，错误发生几率
    influence：修改self.number_sites和self.probability
    """""
    def define(self, number_site, probability):
        assert isinstance(number_site, int)
        assert isinstance(probability, float)
        self.number_site = number_site
        self.probability = probability


    #%%  USER：重载相等运算符
    """""
    input.other：CliffordMajoranaComputer对象，判断两个态矢是否相等
    output：bool对象，判断结果
    """""
    def __eq__(self, other):
        return MajoranaGroup.equal(self.psi, other.psi)


    #%%  USER：初始化方法
    """""
    input.params：int对象，初始化参数
    influence：修改self.psi
    """""
    def initialize(self,params):
        if isinstance(params,np.ndarray) or isinstance(params,list):
            assert len(params)==self.number_site
            stabilizer_vector_new = np.empty(self.number_site, dtype=MajoranaGroup)
            for i in range(self.number_site):
                majorana_vector_temp = np.zeros(self.number_site * 2, dtype=int)
                if params[i]==1:
                    majorana_vector_temp[i * 2] = 1
                    majorana_vector_temp[i * 2 + 1] = 1
                elif params[i]==0:
                    majorana_vector_temp[i * 2] = 0
                    majorana_vector_temp[i * 2 + 1] = 0
                else:
                    raise ValueError("Invalid parameter")
                stabilizer_vector_new[i] = MajoranaGroup()
                stabilizer_vector_new[i].define(majorana_vector_temp,1j)
            self.psi = stabilizer_vector_new


    #%%  USER：执行S量子逻辑门
    """""
    input.index：int对象，量子门作用的site的序号
    influence：将第index个site上的S门作用在self.psi上面，修改self.psi
    """""
    def S(self,index):
        for i in range(self.psi.shape[0]):
            s_0=self.psi[i][2*index]
            s_1=self.psi[i][2*index+1]
            if s_1==1:
                self.psi[i].coff=-self.psi[i].coff


    #%%  USER：执行gamma量子逻辑门
    """""
    input.index：int对象，量子门作用的site的序号
    influence：将第index个site上的gamma门作用在self.psi上面，修改self.psi
    """""
    def gamma(self,index):
        gamma=MajoranaGroup()
        zeros=np.zeros(self.number_site*2, dtype=int)
        zeros[2*index] = 1
        gamma.define(zeros,1)
        for i in range(self.psi.shape[0]):
            self.psi[i]=gamma*self.psi[i]*gamma


    #%%  USER：执行gamma-prime量子门
    """""
    input.index：int对象，量子门作用的site的序号
    influence：将第index个site上的gamma门作用在self.psi上面，修改self.psi
    """""
    def gamma_prime(self,index):
        gamma=MajoranaGroup()
        zeros=np.zeros(self.number_site*2, dtype=int)
        zeros[2*index+1] = 1
        gamma.define(zeros,1)
        for i in range(self.psi.shape[0]):
            self.psi[i]=gamma*self.psi[i]*gamma


    #%%  USER：执行CZ量子逻辑门
    """""
    input.index：int对象，量子门作用的site的序号
    influence：以index_control作为控制位，以index_target，用CZ门修改self.psi
    """""
    def CZ(self,index_0,index_1):
        for i in range(self.psi.shape[0]):
            s_0 = self.psi[i][2 * index_0]
            s_0_prime = self.psi[i][2 * index_0 + 1]
            s_1 = self.psi[i][2 * index_1]
            s_1_prime = self.psi[i][2 * index_1 + 1]
            if s_1==s_0==s_0_prime==s_1_prime==1:
                self.psi[i].coff=-self.psi[i].coff


    #%%  USER：执行BRAID量子逻辑门
    """""
    input.index：int对象，量子门作用的site的序号
    influence：用index_0和index_1上的BRAID门修改self.psi
    """""
    def B(self,index_0,index_1):
        for i in range(self.psi.shape[0]):
            s_0=self.psi[i][2*index_0]
            s_0_prime=self.psi[i][2*index_0+1]
            s_1=self.psi[i][2*index_1]
            s_1_prime=self.psi[i][2*index_1+1]
            if s_0==1 and s_0_prime==0:
                self.psi[i][index_0*2]=1
                self.psi[i][index_0*2+1]=1
                self.psi[i].coff=1j*self.psi[i].coff
                self.psi[i][index_1*2]=np.mod(self.psi[i][index_1*2]+self.psi[i][index_1*2],2)
            elif s_0==0 and s_0_prime==1:
                self.psi[i][index_0*2+1]=1
            if s_1==1 and s_1_prime==0:
                self.psi[i][index_1*2]=1
            elif s_1==0 and s_1_prime==1:
                self.psi[i][index_1*2]=1
                self.psi[i][index_1*2+1]=1
                self.psi[i].coff=1j*self.psi[i].coff
                self.psi[i][index_0*2+1]=np.mod(self.psi[i][index_0*2+1]+self.psi[i][index_0*2+1],2)


    #%%  USER：执行测量
    """""
    input.index：int对象，测量的site
    output：int对象，测量结果
    influence：在第index个site上测量，使self.psi坍缩
    """""
    def measure(self,index):
        flag=-1
        for i in range(self.psi.shape[0]):
            s_0 = self.psi[i][index * 2]
            s_1 = self.psi[i][index * 2 + 1]
            if ((s_0==1 and s_1==0) or (s_0==0 and s_1==1)) and flag==-1:
                flag=i
            elif ((s_0==1 and s_1==0) or (s_0==0 and s_1==1)) and flag!=-1:
                self.psi[i]=self.psi[i]*self.psi[flag]

        if flag==-1:
            return 1

        else:
            if np.random.rand()<0.5:
                coff_new=1
                majorana_vector_new=np.zeros_like(self.psi[0].pauli_vecctor,dtype=int)
                majorana_vector_new[index*2]=1
                majorana_vector_new[index * 2+1] = 1
                stabilizer_new=MajoranaGroup()
                stabilizer_new.define(majorana_vector_new,coff_new)
                self.psi[flag]=stabilizer_new
                return 1
            else:
                coff_new=-1
                majorana_vector_new=np.zeros_like(self.psi[0].pauli_vecctor,dtype=int)
                majorana_vector_new[index*2]=1
                majorana_vector_new[index * 2+1] = 1
                stabilizer_new = MajoranaGroup()
                stabilizer_new.define(majorana_vector_new,coff_new)
                self.psi[flag]=stabilizer_new
                return -1


    #%%  USER：发生量子错误
    """""
    input.args：int or list of int对象，发生量子错误的sites的序号
    influence：按self.probability几率在相应的sites上发生量子错误，修改self.psi
    """""
    def noise(self,*args):
        for i in range(len(args)):
            sample_temp=np.random.rand()
            if sample_temp<self.probability:
                self.gamma(args[i]*2)
            elif self.probability<sample_temp<self.probability*2:
                self.gamma(args[i]*2+1)