import numpy as np


def kinetic(vel, mass):
    return 0.5 * np.sum(mass * (vel**2).sum(1))


def potential(pos, mass, G=1.0, eps=0.0):
    d = pos[None, :, :] - pos[:, None, :]
    r = np.sqrt((d**2).sum(-1) + eps**2)
    iu = np.triu_indices(len(mass), 1)
    return -G * np.sum(mass[iu[0]] * mass[iu[1]] / r[iu])


def total_energy(pos, vel, mass, G=1.0, eps=0.0):
    return kinetic(vel, mass) + potential(pos, mass, G, eps)


def total_momentum(vel, mass):
    return (mass[:, None] * vel).sum(0)


def virial_ratio(pos, vel, mass, G=1.0, eps=0.0):
    """2K/|W|; ~1 for a system in virial equilibrium."""
    return 2 * kinetic(vel, mass) / abs(potential(pos, mass, G, eps))
