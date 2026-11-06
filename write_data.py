"""Generate synthetic India district-level battery waste data.

This file is a PLACEHOLDER for real data. Once official figures are available
from CPCB / MoRTH / state pollution boards, replace data/districts.csv.

Every coefficient below is documented so any figure can be traced.
"""

import csv
import random
from pathlib import Path

random.seed(42)  # deterministic — same data every run

# (state, district, lat, lon, population_millions, urbanization_pct)
DISTRICTS = [
    ("Maharashtra",    "Mumbai",              19.076, 72.877, 20.7,  100),
    ("Maharashtra",    "Pune",                18.520, 73.856,  9.4,   91),
    ("Maharashtra",    "Nagpur",              21.145, 79.088,  4.6,   68),
    ("Maharashtra",    "Nashik",              19.997, 73.789,  6.1,   57),
    ("Karnataka",      "Bengaluru Urban",     12.972, 77.594, 12.3,   91),
    ("Karnataka",      "Mysuru",              12.295, 76.639,  3.0,   60),
    ("Karnataka",      "Hubballi-Dharwad",    15.364, 75.124,  1.8,   55),
    ("Tamil Nadu",     "Chennai",             13.083, 80.271, 10.9,  100),
    ("Tamil Nadu",     "Coimbatore",          11.017, 76.955,  3.5,   79),
    ("Tamil Nadu",     "Madurai",              9.925, 78.119,  3.0,   60),
    ("Delhi",          "New Delhi",           28.614, 77.209, 32.9,   97),
    ("Uttar Pradesh",  "Lucknow",             26.847, 80.947,  4.6,   66),
    ("Uttar Pradesh",  "Kanpur",              26.449, 80.332,  4.6,   65),
    ("Uttar Pradesh",  "Gautam Buddh Nagar",  28.570, 77.320,  1.6,   62),
    ("Gujarat",        "Ahmedabad",           23.023, 72.571,  8.3,   89),
    ("Gujarat",        "Surat",               21.170, 72.831,  7.0,   79),
    ("Rajasthan",      "Jaipur",              26.912, 75.787,  6.6,   65),
    ("West Bengal",    "Kolkata",             22.573, 88.364, 15.3,   88),
    ("Telangana",      "Hyderabad",           17.385, 78.487,  9.5,   92),
    ("Andhra Pradesh", "Visakhapatnam",       17.686, 83.218,  4.3,   57),
    ("Kerala",         "Ernakulam (Kochi)",    9.981, 76.299,  3.4,   68),
    ("Kerala",         "Thiruvananthapuram",   8.524, 76.937,  3.3,   60),
    ("Punjab",         "Ludhiana",            30.901, 75.857,  3.5,   59),
    ("Haryana",        "Gurugram",            28.459, 77.026,  2.5,   84),
    ("Madhya Pradesh", "Indore",              22.720, 75.857,  3.3,   68),
    ("Madhya Pradesh", "Bhopal",              23.259, 77.413,  2.4,   69),
    ("Bihar",          "Patna",               25.594, 85.138,  5.8,   43),
    ("Odisha",         "Bhubaneswar",         20.296, 85.825,  2.1,   55),
    ("Assam",          "Guwahati",            26.145, 91.736,  1.9,   82),
]

CHEMS = ["LFP", "NMC", "NCA", "LMO"]

rows = []
for state, district, lat, lon, pop_m, urb_pct in DISTRICTS:
    # Step 1: Estimate EV fleet in district (in thousands)
    # Assumes ~3 EVs per 1000 urban people (2026 India average, urban-heavy)
    urban_pop_m = pop_m * (urb_pct / 100.0)
    ev_fleet_k = urban_pop_m * 3.0

    # Step 2: Estimate batteries reaching end-of-life this year
    # Assumes ~8% of EV fleet reaches EOL annually
    eol_batteries = int(ev_fleet_k * 1000 * 0.08)

    # Step 3: Average battery mass (kg)
    avg_kg = random.uniform(240, 340)
    total_kg = round(eol_batteries * avg_kg, 1)

    # Chemistry mix (approx Indian market: LFP rising, NMC legacy)
    chem = random.choices(CHEMS, weights=[0.45, 0.35, 0.12, 0.08])[0]

    # Material recovery (typical pyro+hydro process)
    li    = round(total_kg * random.uniform(0.015, 0.022), 1)
    co    = round(total_kg * random.uniform(0.030, 0.060), 1)
    ni    = round(total_kg * random.uniform(0.030, 0.055), 1)
    cu    = round(total_kg * random.uniform(0.060, 0.090), 1)
    al    = round(total_kg * random.uniform(0.100, 0.150), 1)
    graph = round(total_kg * random.uniform(0.140, 0.200), 1)

    rows.append({
        "state": state, "district": district,
        "lat": lat, "lon": lon,
        "population_m": round(pop_m, 1),
        "urbanization_pct": urb_pct,
        "batteries": eol_batteries,
        "total_kg": total_kg,
        "chemistry": chem,
        "li_kg": li, "co_kg": co, "ni_kg": ni,
        "cu_kg": cu, "al_kg": al, "graphite_kg": graph,
    })

out = Path("data/districts.csv")
out.parent.mkdir(exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} districts -> {out}")
print(f"Total batteries: {sum(r['batteries'] for r in rows):,}")
print(f"Total mass:      {sum(r['total_kg'] for r in rows):,.0f} kg")