"""Evolve a Plummer sphere and report energy drift. Usage: python run_plummer.py [N] [steps]"""
import sys

from nbody import plummer, run, total_energy, virial_ratio

n = int(sys.argv[1]) if len(sys.argv) > 1 else 256
steps = int(sys.argv[2]) if len(sys.argv) > 2 else 500
eps, dt = 0.05, 0.01

pos, vel, mass = plummer(n)
E0 = total_energy(pos, vel, mass, eps=eps)
print(f"N={n}  E0={E0:.4f}  virial={virial_ratio(pos, vel, mass, eps=eps):.3f}")
pos, vel = run(pos, vel, mass, dt, steps, eps=eps)
E1 = total_energy(pos, vel, mass, eps=eps)
print(f"after {steps} steps: dE/E={(E1 - E0) / abs(E0):.2e}  virial={virial_ratio(pos, vel, mass, eps=eps):.3f}")
