# astro-lab

Learn astrophysics fundamentals by coding them. Six sessions, then one capstone-style project: a from-scratch N-body simulator (CPU first, GPU stretch).

## Learning path

| # | Topic | Folder | Deliverable | Status | Reading notes (PDF) |
|---|-------|--------|-------------|--------|---------------------|
| 1 | Units, coordinates, time, FITS, Gaia queries | `01_data_and_coordinates/` | `astropy_basics.py` | starter | [session_01](docs/session_01.pdf) |
| 2 | Orbits: leapfrog vs RK4, energy conservation | `02_orbits/` | `kepler_integrators.py` | starter | [session_02](docs/session_02.pdf) |
| 3 | Stellar structure: Lane-Emden, polytropes | `03_stellar_structure/` | `lane_emden.py` | starter | [session_03](docs/session_03.pdf) |
| 4 | Radiative processes: Planck curve, line fitting | `04_radiation/` | TODO | planned | [session_04](docs/session_04.pdf) |
| 5 | Exoplanets: Kepler/TESS light curves, BLS periodogram | `05_lightcurves/` | TODO | planned | [session_05](docs/session_05.pdf) |
| 6 | Hydro: 1D Euler solver (finite volume, Sod shock tube) | `06_hydro_1d/` | TODO | planned | [session_06](docs/session_06.pdf) |
| P | **N-body simulator** (Plummer sphere, softening, diagnostics) | `projects/nbody/` | package + tests + CI | core done | [project_nbody](docs/project_nbody.pdf) |

The PDFs are built from LaTeX sources in `docs/`. For sessions 4-6 they contain theory, an implementation plan and exercises; the code is not written yet. Rebuild with `make -C docs` (needs `latexmk`, `pdflatex`, and the `listings`, `framed` and `booktabs` packages).

Suggested pace: one session per week, ~3 hours each. For every session: read -> implement from scratch -> validate against a library (Astropy, REBOUND, Lightkurve) -> write 5 lines of notes in the folder README.

## Project roadmap (`projects/nbody`)

- [x] Direct-summation O(N^2) forces with Plummer softening
- [x] Kick-drift-kick leapfrog integrator (symplectic)
- [x] Plummer sphere initial conditions
- [x] Diagnostics: energy, momentum, virial ratio
- [x] Unit tests + GitHub Actions CI
- [ ] Adaptive / individual timesteps
- [ ] Barnes-Hut tree (O(N log N))
- [ ] GPU forces via ModernGL compute shader, benchmark vs NumPy
- [ ] Validate against REBOUND on a 3-body figure-eight

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest projects/nbody -q
python 02_orbits/kepler_integrators.py
```

## Publish to GitHub

```bash
cd astro-lab
git init -b main && git add . && git commit -m "Initial commit: learning path + N-body core"
gh repo create astro-lab --public --source=. --push
```

## Resources

- learn.astropy.org (tutorials)
- Lightkurve tutorials (Kepler/TESS)
- REBOUND docs (N-body reference)
- Zingale, *Computational Astrophysics* notes (hydro)
- Ivezic et al., *Statistics, Data Mining, and Machine Learning in Astronomy*
