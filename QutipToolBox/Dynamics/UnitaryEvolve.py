from qutip import *


def unitary_evolve(model, psi, t_list, Expectation_list, Collapse_list,*args):
    if len(args)!=0:
        function_list=args[0]
        operator_list=args[1]
        parameter_list=args[2]
        H_time=[model.H]
        for i in range(len(function_list)):
            H_time.append([function_list[i],operator_list[i]])
        result_list=mesolve(H_time,psi,t_list,Collapse_list,Expectation_list,parameter_list).expect
        psi_result=mesolve(H_time,psi,t_list,Collapse_list,parameter_list).state[-1]
    else:
        result_list=mesolve(model.H,psi,t_list,Collapse_list,Expectation_list).expect
        psi_result=mesolve(model.H,psi,t_list,Collapse_list).states[-1]
    return result_list, psi_result