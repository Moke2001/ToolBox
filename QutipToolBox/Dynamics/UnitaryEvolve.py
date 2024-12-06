from qutip import *


def unitary_evolve(model, psi, t_list, Expectation_list):
    result_list=mesolve(H=model.get_H(),rho0=psi,tlist=t_list,c_ops=model.get_C(),e_ops=Expectation_list,args=model.get_function_params()).expect
    psi_result=mesolve(H=model.get_H(),rho0=psi,tlist=t_list,c_ops=model.get_C(),args=model.get_function_params()).states[-1]
    return result_list, psi_result