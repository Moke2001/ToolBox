from qutip import identity, tensor


def operator_generator(N,operator,index):
    result=None
    for i in range(N):
        if i == 0:
            if i == index:
                result = operator
            else:
                result = identity(2)
        else:
            if i == index:
                result = tensor(result, operator)
            else:
                result = tensor(result, identity(2))
    return result