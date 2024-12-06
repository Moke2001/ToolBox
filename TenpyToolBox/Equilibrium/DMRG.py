from tenpy.algorithms import dmrg
from TenpyToolBox.ModelPackage.ModelPackage import ModelPackage


def DMRG(model):
    assert isinstance(model, ModelPackage)
    psi = model.state_creator('random',10)
    dmrg_params = {
        'mixer': None,
        'max_E_err': 1.e-10,
        'trunc_params': {
            'chi_max': 30,
            'svd_min': 1.e-10
        },
        'combine': True
    }
    info = dmrg.run(psi, model.get_model(), dmrg_params)  # the main work...
    return info['E'],psi