"""Session 3: Lane-Emden equation  (1/x^2) d/dx (x^2 dθ/dx) = -θ^n.
Checks: n=0, 1, 5 have analytic solutions. Prints first zero ξ1 (stellar surface).
"""
import numpy as np
from scipy.integrate import solve_ivp


def solve(n, x_max=50.0):
    def rhs(x, y):
        th, dth = y
        return [dth, -max(th, 0.0) ** n - 2.0 * dth / x]

    x0 = 1e-6
    th0 = 1 - x0**2 / 6  # series start avoids the x=0 singularity
    dth0 = -x0 / 3
    hit = lambda x, y: y[0]
    hit.terminal, hit.direction = True, -1
    sol = solve_ivp(rhs, [x0, x_max], [th0, dth0], events=hit, rtol=1e-10, atol=1e-12, dense_output=True)
    return sol


if __name__ == "__main__":
    analytic = {0: np.sqrt(6), 1: np.pi}
    for n in (0, 1, 1.5, 3, 4):
        xi1 = solve(n).t_events[0][0]
        ref = f"  (analytic {analytic[n]:.5f})" if n in analytic else ""
        print(f"n={n}: xi1={xi1:.5f}{ref}")
    # known: n=1.5 -> 3.65375, n=3 -> 6.89685 (Eddington standard model)
