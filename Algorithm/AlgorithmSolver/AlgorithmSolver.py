import numpy as np
from Algorithm.AlgorithmQutip.ApplyQutip import apply_qutip
from Algorithm.AlgorithmQutip.EnergySpectrumSolverQutip import energy_spectrum_solver_qutip
from Algorithm.AlgorithmQutip.EvolutionSolverQutip import evolution_solver_qutip
from Algorithm.AlgorithmQutip.ExpectationQutip import expectation_qutip
from Algorithm.AlgorithmQutip.GroundStateSolverQutip import ground_state_solver_qutip
from Algorithm.AlgorithmQutip.MeasurementSimulatorQutip import measurement_simulator_qutip
from Algorithm.AlgorithmQutip.OverlapQutip import overlap_qutip
from Algorithm.AlgorithmTenpy.EnergySpectrumSolverTenpy import energy_spectrum_solver_tenpy
from Algorithm.AlgorithmTenpy.EvolutionSolverTenpy import evolution_solver_tenpy
from Algorithm.AlgorithmTenpy.ExpectationTenpy import expectation_tenpy
from Algorithm.AlgorithmTenpy.GroundStateSolverTenpy import ground_state_solver_tenpy
from Algorithm.AlgorithmTenpy.MeasurementSimulatorTenpy import measurement_simulator_tenpy
from Algorithm.AlgorithmTenpy.OverlapTenpy import overlap_tenpy
from Format.ModelFormat.ModelFormat import ModelFormat


class AlgorithmSolver:
    @staticmethod
    def EnergySpectrumSolver(model,solver):
        assert isinstance(model,ModelFormat)
        assert isinstance(solver,str)
        if solver=='qutip':
            return energy_spectrum_solver_qutip(model)
        elif solver=='tenpy':
            return energy_spectrum_solver_tenpy(model)


    @staticmethod
    def EvolutionSolver(model,psi_initial,expectation_terms,t_list,solver):
        assert isinstance(model,ModelFormat)
        assert isinstance(expectation_terms,list)
        assert isinstance(t_list,np.ndarray)
        assert isinstance(solver,str)
        if solver=='qutip':
            return evolution_solver_qutip(model,psi_initial,expectation_terms,t_list)
        elif solver=='tenpy':
            return evolution_solver_tenpy(model, psi_initial, expectation_terms, t_list)


    @staticmethod
    def GroundStateSolver(model,solver):
        assert isinstance(model,ModelFormat)
        assert isinstance(solver,str)
        if solver=='qutip':
            return ground_state_solver_qutip(model)
        elif solver=='tenpy':
            return ground_state_solver_tenpy(model)


    @staticmethod
    def MeasurementSimulator(model, psi_initial, projector_list, eigenvalue_list,solver):
        assert isinstance(model,ModelFormat)
        assert isinstance(projector_list,list)
        assert isinstance(eigenvalue_list,list)
        assert isinstance(solver,str)
        if solver=='qutip':
            return measurement_simulator_qutip(model,psi_initial,projector_list,eigenvalue_list)
        elif solver=='tenpy':
            return measurement_simulator_tenpy(model, psi_initial, projector_list, eigenvalue_list)


    @staticmethod
    def Apply(model_format,state_initial,term,normalize,solver):
        if solver=='qutip':
            return apply_qutip(model_format,state_initial,term,normalize)
        elif solver=='tenpy':
            return apply_qutip(model_format,state_initial,term,normalize)


    @staticmethod
    def Expectation(model_format,state_initial,term,solver):
        if solver=='qutip':
            return expectation_qutip(model_format,state_initial,term)
        elif solver=='tenpy':
            return expectation_tenpy(model_format,state_initial,term)


    @staticmethod
    def Overlap(model_format,state_0,state_1,solver):
        if solver=='qutip':
            return overlap_qutip(model_format,state_0,state_1)
        elif solver=='tenpy':
            return overlap_tenpy(model_format,state_0,state_1)
