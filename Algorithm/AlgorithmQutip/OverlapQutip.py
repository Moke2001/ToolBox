from State.StatePreparer.StatePreparer import state_preparer


def overlap_qutip(model_format,state_0,state_1):
    psi_0=state_preparer(model_format,state_0,'qutip')
    psi_1=state_preparer(model_format,state_1,'qutip')
    return psi_1.vector.overlap(psi_0.vector)
