import numpy as np


def circular_binary(m1=1.0, m2=1.0, sep=1.0, G=1.0):
    """Two bodies on a circular orbit, centre of mass at rest at the origin."""
    mass = np.array([m1, m2])
    M = m1 + m2
    pos = np.array([[-m2 / M * sep, 0, 0], [m1 / M * sep, 0, 0]], dtype=float)
    v_rel = np.sqrt(G * M / sep)
    vel = np.array([[0, -m2 / M * v_rel, 0], [0, m1 / M * v_rel, 0]], dtype=float)
    return pos, vel, mass


def plummer(n, a=1.0, M=1.0, G=1.0, seed=0):
    """Plummer sphere (Aarseth, Henon & Wielen 1974), recentred to COM frame."""
    rng = np.random.default_rng(seed)
    mass = np.full(n, M / n)

    u = rng.uniform(1e-4, 1 - 1e-4, n)
    r = a / np.sqrt(u ** (-2 / 3) - 1)
    pos = r[:, None] * _unit_vectors(rng, n)

    # speed: rejection-sample q with g(q) = q^2 (1-q^2)^3.5
    q = np.empty(n)
    i = 0
    while i < n:
        x, y = rng.uniform(0, 1), rng.uniform(0, 0.1)
        if y < x**2 * (1 - x**2) ** 3.5:
            q[i] = x
            i += 1
    v_esc = np.sqrt(2 * G * M) * (r**2 + a**2) ** -0.25
    vel = (q * v_esc)[:, None] * _unit_vectors(rng, n)

    pos -= np.average(pos, axis=0, weights=mass)
    vel -= np.average(vel, axis=0, weights=mass)
    return pos, vel, mass


def _unit_vectors(rng, n):
    z = rng.uniform(-1, 1, n)
    phi = rng.uniform(0, 2 * np.pi, n)
    s = np.sqrt(1 - z**2)
    return np.stack([s * np.cos(phi), s * np.sin(phi), z], axis=1)
