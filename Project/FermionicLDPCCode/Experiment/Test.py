from Physics.QuantumComputation.Code.ClassicalCode.DualContainingCode import DualContainingCode
from Physics.QuantumComputation.Code.QuantumCode.PauliCode.CSSCode import CSSCode
from Physics.QuantumComputation.Code.QuantumCode.Transformer.Css2Majorana import css2majorana

if __name__=='__main__':
    EC=DualContainingCode(3,2)
    CSS=CSSCode(EC,EC)
    majorana_code=css2majorana(CSS)
    x=majorana_code.get_logical_operator()
    pass