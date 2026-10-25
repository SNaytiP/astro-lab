import numpy as np


def accelerations(pos, mass, G=1.0, eps=0.0):
    """Direct O(N^2) accelerations with Plummer softening eps. pos: (N,3), mass: (N,)."""
    d = pos[None, :, :] - pos[:, None, :]          # d[i,j] = r_j - r_i
    r2 = (d**2).sum(-1) + eps**2
    np.fill_diagonal(r2, np.inf)                   # no self-force
    inv_r3 = r2**-1.5
    return G * (d * (mass[None, :, None] * inv_r3[:, :, None])).sum(1)
