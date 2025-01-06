from qutip import basis, tensor


def state_generator(N,state_list):
    result=None
    for i in range(N):
        if i == 0:
            result=basis(2,state_list[i])
        else:
            result=tensor(result, basis(2,state_list[i]))
    return result