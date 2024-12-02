from tenpy.algorithms import tdvp

from TenpyToolBox.Package.ModelPackage.ModelPackage import ModelPackage


def evolve_tdvp(dt, N_steps, chi_max, psi_origin, model:ModelPackage):
    ##  TDVP执行参数
    tdvp_params = {
        'start_time': 0,
        'dt': dt,
        'N_steps': N_steps,
        'trunc_params': {
            'chi_max': chi_max,
            'svd_min': 1.e-10,
            'trunc_cut': None
        }
    }
    psi_result=psi_origin.copy()
    tdvp_engine = tdvp.TimeDependentTwoSiteTDVP(psi_result, model.get_model(), tdvp_params)
    tdvp_engine.run()

    return psi_result