"""Session 2: leapfrog vs RK4 on an eccentric Kepler orbit. Units G*M = 1.
Expect: RK4 is far more accurate per step at small dt, but its energy error grows
secularly; leapfrog's error is larger but stays bounded (symplectic), so it wins
over long runs. Try dt=0.01 vs dt=0.05 and see where the curves cross.
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def acc(r):
    return -r / np.linalg.norm(r) ** 3


def energy(r, v):
    return 0.5 * v @ v - 1.0 / np.linalg.norm(r)


def leapfrog(r, v, dt, n):
    out = np.empty(n)
    a = acc(r)
    for i in range(n):
        v = v + 0.5 * dt * a
        r = r + dt * v
        a = acc(r)
        v = v + 0.5 * dt * a
        out[i] = energy(r, v)
    return out


def rk4(r, v, dt, n):
    out = np.empty(n)
    for i in range(n):
        k1r, k1v = v, acc(r)
        k2r, k2v = v + 0.5 * dt * k1v, acc(r + 0.5 * dt * k1r)
        k3r, k3v = v + 0.5 * dt * k2v, acc(r + 0.5 * dt * k2r)
        k4r, k4v = v + dt * k3v, acc(r + dt * k3r)
        r = r + dt / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        out[i] = energy(r, v)
    return out


if __name__ == "__main__":
    e = 0.6
    r0 = np.array([1 - e, 0.0])  # pericentre, a = 1
    v0 = np.array([0.0, np.sqrt((1 + e) / (1 - e))])
    E0 = energy(r0, v0)
    dt, orbits = 0.05, 1000  # coarse dt on purpose: RK4 is more accurate per step but drifts
    n = int(orbits * 2 * np.pi / dt)

    lf = np.abs((leapfrog(r0, v0, dt, n) - E0) / E0)
    rk = np.abs((rk4(r0, v0, dt, n) - E0) / E0)
    print(f"max |dE/E| after {orbits} orbits: leapfrog={lf.max():.2e}  rk4={rk.max():.2e}")

    # per-orbit maximum, otherwise the oscillating leapfrog error fills the plot
    w = int(round(2 * np.pi / dt))
    m = n // w
    env = lambda x: x[: m * w].reshape(m, w).max(axis=1)
    orbit_no = np.arange(1, m + 1)
    plt.semilogy(orbit_no, env(lf), label="leapfrog")
    plt.semilogy(orbit_no, env(rk), label="RK4")
    plt.xlabel("orbits")
    plt.ylabel("max |dE/E| per orbit")
    plt.legend()
    plt.title(f"Kepler orbit e={e}, dt={dt}")
    import pathlib
    plt.savefig(pathlib.Path(__file__).with_name("energy_drift.png"), dpi=150, bbox_inches="tight")
