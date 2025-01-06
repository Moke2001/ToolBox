from qutip import *
from QuantumComputation.QuantumProcessor.ErrorModel.ErrorModel import ErrorModel
from QuantumComputation.QuantumProcessor.ErrorModel.FermionicGateErrorModel import FermionicGateErrorModel
from QuantumComputation.Helper.OperatorGenerator import operator_generator
from QuantumComputation.QuantumProcessor.PhysicalProcessor.PhysicalProcessor import PhysicalProcessor
from QuantumComputation.Helper.StateGenerator import state_generator


class RydbergFermionProcessor(PhysicalProcessor):
    def __init__(self, number_locality):
        super().__init__(number_locality)

    def gate(self,gate_name,*args):
        if gate_name == 'I':
            return operator_generator(self.N,identity(2),0)
        elif gate_name == 'Interaction':
            n_0=fcreate(self.N,args[0])*fdestroy(self.N,args[0])
            n_1=fcreate(self.N,args[1])*fdestroy(self.N,args[1])
            return (1j*n_0*n_1*args[2]).expm()
        elif gate_name == 'Tunneling':
            term_0=fcreate(self.N,args[0])*fdestroy(self.N,args[1])
            term_1=fcreate(self.N,args[1])*fdestroy(self.N,args[0])
            return (1j * term_0 * term_1 * args[2]).expm()
        elif gate_name == 'Phase':
            return (1j*fcreate(self.N,args[0])*fdestroy(self.N,args[0])*args[1]).expm()

    def measure(self,measure_name,*args):
        if measure_name == 'MeasureNumber':
            PN=operator_generator(self.N,fcreate(self.N,args[0])*fdestroy(self.N,args[0]),args[0])
            eigenvalues,eigenstates=PN.eigenstates()
        else:
            raise TypeError('不存在这样的测量类型')
        return eigenvalues,eigenstates

    def initialize(self,method,*args):
        if method == 'trivial':
            return state_generator(self.N,args[0])

    def get_error(self,name,*args):
        if name == 'I':
            return ErrorModel(self.N,[self.gate('I')])
        elif name == 'Phase':
            return FermionicGateErrorModel(self.N,0.01,args[0])
        elif name == 'Interaction' or args[0] == 'Tunneling':
            return FermionicGateErrorModel(self.N,0.02,args[0],args[1])
        elif name == 'MeasureNumber':
            return FermionicGateErrorModel(self.N,0.01,args[0])