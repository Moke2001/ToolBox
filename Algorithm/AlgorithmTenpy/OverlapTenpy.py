from State.StatePreparer.StatePreparer import state_preparer


def overlap_tenpy(model_format,state_0,state_1):
    psi_0=state_preparer(model_format,state_0,'tenpy')
    psi_1=state_preparer(model_format,state_1,'tenpy')
    return psi_1.mps.overlap(psi_0.mps)