

def blockade(psi,subspace_projector_list):
    psi_result=None
    for i in range(len(subspace_projector_list)):
        if i==0:
            psi_result=subspace_projector_list[i]*psi
        else:
            psi_result=psi_result+subspace_projector_list[i]*psi
    if psi_result.norm()==0:
        return False
    else:
        psi_result=psi_result/psi_result.norm()
        return psi_result