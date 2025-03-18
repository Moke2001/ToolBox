import galois
import numpy as np
import random
from Physics.QuantumComputation.Code.ClassicalCode.LinearCode import LinearCode


class DualContainingCode(LinearCode):
    def __init__(self,m,s):
        super().__init__()
        H_dual = self.generate_eg_ii_ldpc(m, s)
        for i in range(H_dual.shape[0]):
            self.push_checker(H_dual[i])


    def generate_eg_ii_ldpc(self,m, s):
        """
        Generates the dual-containing LDPC code (EG-II) parity-check matrix based on Euclidean Geometry.

        Parameters:
        m (int): Dimension of the Euclidean Geometry.
        s (int): Exponent such that q = 2^s, defining the finite field GF(q).

        Returns:
        np.ndarray: The dual-containing parity-check matrix H_dual.
        """
        q = 2 ** s
        n_points = q ** m
        GF = galois.GF(q ** m, repr="power")  # Use power representation for clarity
        primitive_element = GF.primitive_element

        # Generate non-origin points: α^0, α^1, ..., α^(n_points-2)
        non_origin_points = [primitive_element ** i for i in range(n_points - 1)]

        # Calculate number of cyclic classes J
        J = (q ** (m - 1) - 1) // (q - 1)

        # Placeholder for cyclic classes' base vectors (to be implemented based on EG lines)
        # This example uses random vectors for demonstration; replace with actual line generation
        H_blocks = []
        for _ in range(J):
            # Generate a random base incidence vector (simulating a line's incidence)
            # In practice, generate this based on EG(m, q) lines
            base_vector = np.zeros(len(non_origin_points), dtype=int)
            # Simulate a line with q points (randomly chosen for illustration)
            indices = np.random.choice(len(non_origin_points), size=q, replace=False)
            base_vector[indices] = 1
            # Create circulant matrix from the base vector
            H_j = self.circulant_matrix(base_vector)
            H_blocks.append(H_j)

        # Construct H_dual = [H_1^T | H_2^T | ... | H_J^T | H_1 | H_2 | ... | H_J]
        H_left = np.hstack([H_j.T for H_j in H_blocks])  # Transposed blocks
        H_right = np.hstack(H_blocks)  # Original blocks
        H_dual = np.hstack([H_left, H_right])

        return H_dual

    def circulant_matrix(self,vector):
        """Generates a circulant matrix from a base vector."""
        n = len(vector)
        matrix = np.zeros((n, n), dtype=int)
        for i in range(n):
            matrix[i] = np.roll(vector, i)
        return matrix