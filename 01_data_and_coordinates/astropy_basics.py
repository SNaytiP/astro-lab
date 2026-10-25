"""Session 1: units, coordinates, time. Offline; Gaia query is at the bottom (needs network)."""
import astropy.units as u
from astropy.constants import G, M_sun, au
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time

# Units: orbital period of Earth from Kepler's third law
a = 1 * u.au
P = (2 * 3.141592653589793 * (a**3 / (G * M_sun)) ** 0.5).to(u.day)
print(f"Earth period: {P:.2f}")  # ~365.25 d

# Coordinates: Sirius in ICRS -> Galactic
sirius = SkyCoord("06h45m08.9s", "-16d42m58s", frame="icrs")
print("Galactic l,b:", sirius.galactic.l.deg, sirius.galactic.b.deg)

# Altitude from Bangkok right now
bkk = EarthLocation(lat=13.75 * u.deg, lon=100.5 * u.deg, height=2 * u.m)
now = Time.now()
altaz = sirius.transform_to(AltAz(obstime=now, location=bkk))
print(f"Sirius altitude from Bangkok at {now.iso}: {altaz.alt:.1f}")

# Time scales
t = Time("2026-10-25 00:00:00", scale="utc")
print("JD:", t.jd, "| TDB:", t.tdb.iso)

# Gaia query (uncomment with network access):
# from astroquery.gaia import Gaia
# job = Gaia.launch_job("SELECT TOP 1000 source_id, ra, dec, parallax, phot_g_mean_mag, bp_rp "
#                       "FROM gaiadr3.gaia_source WHERE parallax_over_error > 10")
# df = job.get_results().to_pandas()
# -> plot bp_rp vs absolute mag (G + 5*log10(parallax/100)) for the HR diagram
