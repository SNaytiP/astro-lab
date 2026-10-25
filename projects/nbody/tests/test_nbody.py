import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from nbody import (accelerations, run, plummer, circular_binary,
                   total_energy, total_momentum, virial_ratio)


def test_binary_energy_conserved():
    pos, vel, mass = circular_binary()
    E0 = total_energy(pos, vel, mass)
    period = 2 * np.pi * np.sqrt(1.0 / 2.0)  # a^3 / (G*M), M=2
    steps = int(10 * period / 0.001)
    pos, vel = run(pos, vel, mass, 0.001, steps)
    assert abs((total_energy(pos, vel, mass) - E0) / E0) < 1e-6


def test_binary_returns_to_start():
    pos0, vel, mass = circular_binary()
    period = 2 * np.pi * np.sqrt(1.0 / 2.0)
    steps = int(round(period / 0.0005))
    pos, _ = run(pos0.copy(), vel, mass, period / steps, steps)
    assert np.allclose(pos, pos0, atol=1e-5)


def test_momentum_conserved_plummer():
    pos, vel, mass = plummer(64, seed=1)
    p0 = total_momentum(vel, mass)
    pos, vel = run(pos, vel, mass, 0.01, 100, eps=0.05)
    assert np.allclose(total_momentum(vel, mass), p0, atol=1e-10)


def test_newton_third_law():
    rng = np.random.default_rng(0)
    pos, mass = rng.normal(size=(20, 3)), rng.uniform(0.5, 2, 20)
    a = accelerations(pos, mass, eps=0.01)
    assert np.allclose((mass[:, None] * a).sum(0), 0, atol=1e-12)


def test_plummer_roughly_virialised():
    pos, vel, mass = plummer(2000, seed=3)
    assert 0.8 < virial_ratio(pos, vel, mass) < 1.2
