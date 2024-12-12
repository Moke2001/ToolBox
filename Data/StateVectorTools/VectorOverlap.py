import qutip


def vector_overlap(psi_0,psi_1):
    assert isinstance(psi_0, qutip.Qobj) and isinstance(psi_1, qutip.Qobj)
    return psi_0.dag() * psi_1