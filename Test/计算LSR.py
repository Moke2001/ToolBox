import itertools
import numpy as np
from matplotlib import pyplot as plt
from qutip import *

def plot_deltaE(Es, x_max, n_space):
    # Ensure Es is a 1D array
    Es = np.array(Es).flatten()
    Es.sort()

    # Calculate delta E
    delta = Es[1:] - Es[:-1]
    delta /= np.mean(delta)

    # Filter delta values
    select_delta = delta[delta < x_max]

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # First subplot (Histogram of delta E)
    axs[0].hist(select_delta, bins=n_space, density=True, alpha=0.7, color='grey')
    axs[0].set_xlim([0, x_max])

    xs = np.linspace(0, x_max, n_space)
    ys_poisson = get_poisson(xs / np.mean(delta))
    ys_goe = get_goe(xs / np.mean(delta))

    axs[0].plot(xs, ys_poisson, 'r-', linewidth=2, label='Poisson')
    axs[0].plot(xs, ys_goe, 'b-', linewidth=2, label='GOE')
    axs[0].set_title(f'lsr={calc_LSR(Es)}')
    axs[0].set_xlabel(r'$\Delta E$')
    axs[0].set_ylabel(r'$P(\Delta E)$')
    axs[0].tick_params(axis='both', which='major', labelsize=15)
    axs[0].legend()

    # Second subplot (Histogram of Es)
    axs[1].hist(Es, bins=50, density=True, alpha=0.7, color='grey')
    axs[1].set_xlabel(r'$E$')
    axs[1].set_ylabel(r'$D(E)$')
    axs[1].tick_params(axis='both', which='major', labelsize=15)

    plt.tight_layout()
    plt.show()

    return fig

def get_poisson(s):
    return np.exp(-s)

def get_goe(s):
    return (np.pi / 2) * s * np.exp(-np.pi / 4 * (s**2))

def calc_LSR(Es):
    # Placeholder function for the MATLAB calc_LSR
    # You need to implement this function based on your specific requirements
    return np.var(Es) / np.mean(np.diff(Es))  # Example implementation


def LSR(Es):
    Es = np.ravel(Es)

    # Sort the array
    Es = np.sort(Es)

    # Calculate differences between consecutive elements
    delta = Es[1:] - Es[:-1]

    # Construct the "t" array
    t = np.column_stack((delta[:-1], delta[1:]))

    # Calculate LSR
    LSR = np.min(t, axis=1) / np.max(t, axis=1)

    # Calculate mean of LSR
    LSR_mean = np.mean(LSR)

    return LSR_mean

def sigma(type,index,N):
    if type == 'x':
        result = sigmax()
    elif type == 'y':
        result = sigmay()
    elif type == 'z':
        result = sigmaz()
    elif type == 'i':
        result = identity(2)
    else:
        raise TypeError
    temp=None
    for i in range(N):
        if i==0:
            if i==index:
                temp=result
            else:
                temp=identity(2)
        else:
            if i==index:
                temp=tensor(temp,result)
            else:
                temp=tensor(temp,identity(2))
    return temp

def generate_binary_lists(N):
    return [list(combination) for combination in itertools.product([0, 1], repeat=N)]

def basis_creator(p_state):
    assert isinstance(p_state, list)
    psi=None
    for i in range(len(p_state)):
        if i==0:
            psi=basis(2,p_state[i])
        else:
            psi=tensor(psi,basis(2,p_state[i]))
    return psi

def reflection(N):
    p_list=generate_binary_lists(N)
    R=0
    for i in range(len(p_list)):
        R=R+basis_creator(p_list[i])*basis_creator(p_list[i][::-1]).dag()
    return R

def flip(N):
    F=sigmax()
    for i in range(N-1):
        F=tensor(F,sigmax())
    return F

def projector(N,H):
    F=flip(N)
    R=reflection(N)
    F_eigenvalues, F_eigenvectors = F.eigenstates()
    R_eigenvalues, R_eigenvectors = R.eigenstates()
    F_projector=0
    for i in range(len(F_eigenvalues)):
        if np.abs(F_eigenvalues[i]-F_eigenvalues[1])<=0.001:
            F_projector=F_projector+F_eigenvectors[i]*F_eigenvectors[i].dag()
    R_projector=0
    for i in range(len(R_eigenvalues)):
        if np.abs(R_eigenvalues[i]-R_eigenvalues[-1])<=0.001:
            R_projector=R_projector+R_eigenvectors[i]*R_eigenvectors[i].dag()

    return F_projector*R_projector

def main(J_2,N):
    H=0
    ##  TFIM-ZZ项
    J = 1
    for i in range(N-1):
        H=H-J*sigma('z',i,N)*sigma('z',i+1,N)

    ##  TFIM-X项
    gamma = 0.05
    for i in range(N):
        H = H-gamma*sigma('x',i,N)

    ##  修正XX项
    gamma_2 = 0

    ##  修正ZZ-2项
    for i in range(N-2):
        H=H-J_2*sigma('z',i,N)*sigma('z',i+2,N)

    P=projector(N,H)
    H=P*H*(P.dag())
    rank=np.linalg.matrix_rank(H.full())
    eigenvalues,eigenstates=H.eigenstates()
    result=[]
    for i in range(len(eigenvalues)):
        if np.abs(eigenvalues[i])>0.000001:
            result.append(eigenvalues[i])
    assert rank==len(result)
    temp=LSR(result)
    print(temp)
    return temp


if __name__ == '__main__':
    main(0.5,12)

