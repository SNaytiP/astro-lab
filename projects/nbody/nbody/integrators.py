import numpy as np
from .forces import accelerations


def leapfrog_step(pos, vel, mass, dt, acc=None, G=1.0, eps=0.0):
    """One kick-drift-kick step. Returns (pos, vel, acc) so acc can be reused."""
    if acc is None:
        acc = accelerations(pos, mass, G, eps)
    vel = vel + 0.5 * dt * acc
    pos = pos + dt * vel
    acc = accelerations(pos, mass, G, eps)
    vel = vel + 0.5 * dt * acc
    return pos, vel, acc


def run(pos, vel, mass, dt, steps, G=1.0, eps=0.0, every=1, callback=None):
    """Integrate `steps` steps; call callback(step, pos, vel) every `every` steps."""
    acc = None
    for k in range(1, steps + 1):
        pos, vel, acc = leapfrog_step(pos, vel, mass, dt, acc, G, eps)
        if callback and k % every == 0:
            callback(k, pos, vel)
    return pos, vel
