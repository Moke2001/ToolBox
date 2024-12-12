from qutip import expect
from Data.StateVectorTools.Term2Qobj import term2qobj


def vector_expectation(model,vector,term):
    return expect(term2qobj(term, model), vector)