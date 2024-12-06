import numpy as np
from qutip import *


def reflection_operator(n):
    indices = list(range(n))
    indices.reverse()
    swap_ops = [swap(i, j) for i, j in zip(range(n), indices)]
    reflection_op = swap_ops[0]
    for op in swap_ops[1:]:
        reflection_op = reflection_op * op
    return reflection_op

if __name__=='__main__':
    # 示例：假设我们有一个2量子比特系统
    # 定义哈密顿量
    H = tensor(sigmaz(), sigmaz()) + 0.5 * (tensor(sigmax(), qeye(2)) + tensor(qeye(2), sigmax()))

    # 定义一个对称性操作，例如交换两个量子比特（在这个简单例子中）
    P = swap(2)

    # 对哈密顿量和对称性操作一起对角化
    evals, estates = (H.transform(P)).eigenstates()

    # 选择一个特定的sector，本例假设选择eigenvalue=1，对应对称性+1的sector
    target_sector = 1
    selected_evals = []
    selected_estates = []

    for i, eval in enumerate(evals):
        if np.isclose(eval, target_sector):
            selected_evals.append(eval)
            selected_estates.append(estates[i])

    print("Selected Eigenvalues:", selected_evals)
    print("Selected Eigenstates:", selected_estates)



