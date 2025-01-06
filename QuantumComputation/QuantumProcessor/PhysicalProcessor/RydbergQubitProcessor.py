import numpy as np
from qutip import *
from scipy.linalg import hadamard
from QuantumComputation.QuantumProcessor.ErrorModel.ErrorModel import ErrorModel
from QuantumComputation.QuantumProcessor.ErrorModel.PauliGateErrorModel import PauliGateErrorModel
from QuantumComputation.Helper.OperatorGenerator import operator_generator
from QuantumComputation.QuantumProcessor.PhysicalProcessor.PhysicalProcessor import PhysicalProcessor
from QuantumComputation.Helper.StateGenerator import state_generator


class RydbergQubitProcessor(PhysicalProcessor):
    def __init__(self, number_locality):
        super().__init__(number_locality)

    def gate(self,gate_name,*args):
        if gate_name == 'X':
            return operator_generator(self.N,sigmax(),args[0])
        elif gate_name == 'Y':
            return operator_generator(self.N,sigmay(),args[0])
        elif gate_name == 'Z':
            return operator_generator(self.N,sigmaz(),args[0])
        elif gate_name == 'I':
            return operator_generator(self.N,identity(2),0)
        elif gate_name == 'H':
            return operator_generator(self.N,Qobj(hadamard(2)),args[0])
        elif gate_name == 'S':
            return operator_generator(self.N,Qobj(np.array([[1,0],[0,1j]])),args[0])
        elif gate_name == 'T':
            return operator_generator(self.N, Qobj(np.array([[1, 0],[0,np.exp(1j*np.pi/4)]])), args[0])
        elif gate_name == 'CZ':
            term_0 = self.gate('I',args[0])*self.gate('I',args[1])
            term_1 = self.gate('I',args[0]) * self.gate('Z',args[1])
            term_2 = self.gate('Z', args[0]) * self.gate('I', args[1])
            term_3 = -self.gate('Z', args[0]) * self.gate('Z', args[1])
            return 0.5*(term_0+term_1 + term_2+term_3)

    def measure(self,name,*args):
        if name == 'MeasureZ':
            Z=operator_generator(self.N,sigmax(),args[0])
            eigenvalues,eigenstates=Z.eigenstates()
        elif name == 'MeasureX':
            X=operator_generator(self.N,sigmax(),args[0])
            eigenvalues,eigenstates=X.eigenstates()
        elif name == 'MeasureString':
            operator_string=args[0]
            op=1
            for i in range(len(operator_string)):
                if operator_string[i] == 'X':
                    op=op*operator_generator(self.N,sigmax(),i)
                elif operator_string[i] == 'Y':
                    op=op*operator_generator(self.N,sigmay(),i)
                elif operator_string[i] == 'Z':
                    op=op*operator_generator(self.N,sigmaz(),i)
                elif operator_string[i] == 'I':
                    op=op*operator_generator(self.N,identity(2),i)
            eigenvalues, eigenstates = op.eigenstates()
        else:
            raise TypeError('不存在这样的测量类型')

        return eigenvalues,eigenstates

    def get_error(self,name,*args):
        if args[0] == 'I':
            return ErrorModel(self.N,[self.gate('I')])
        elif args[0] == 'X' or args[0] == 'Y' or args[0] == 'Z' or args[0] == 'H' or args[0] == 'S':
            return PauliGateErrorModel(self.N,0.01,args[0])
        elif args[0] == 'T':
            return PauliGateErrorModel(self.N,0.02,args[0])
        elif args[0] == 'CZ':
            return PauliGateErrorModel(self.N,0.03,args[0],args[1])
        elif args[0] == 'MeasureZ':
            return PauliGateErrorModel(self.N, 0.01, args[0])
        elif args[0] == 'MeasureX':
            return PauliGateErrorModel(self.N, 0.01, args[0])


    def initialize(self,method):
        if method == 'trivial':
            return state_generator(self.N,[0]*self.N)