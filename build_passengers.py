#!/usr/bin/env python3
"""
build_passengers.py  -- Pax Forecast Model, Step 1: construct the passenger universe.

Reads the foundation departure schedule (asimplied.csv, one row per flight) and
emits passengers.csv: one row per passenger pax = 1..N, each assigned to exactly one
flight (a many-to-one assignment). Passengers are enumerated flight by flight in
departure-time (dep / SOBT) order, so pax 1 is the first seat of the first flight and
pax N is the last seat of the last flight.

Canonical variables (defined by Yash Moitra):
  flight : flight designator,  e.g. "AI 101"        (string)
  n      : flight serial no.,  1 <= n <= n_last      (integer)
  route  : routing,            "DEL-...-XYZ"          (string)
  dest   : final destination,  "XYZ"                  (3-letter IATA)
  cap    : seats / capacity,   cap >= 1               (integer)
  dep    : departure time,     0000 <= dep <= 2359    (HHMM, 24h clock)
Step-1 additions:
  pax            : passenger index, 1 <= pax <= N
  seat_on_flight : seat ordinal within a flight, 1 <= seat_on_flight <= cap

Assumption 1 (universe construction): one seat == one passenger (load factor = 1).
Load factors / no-shows are applied in a later step, not here.

Data treatment: flight B4 443 (Beond, DEL-MLE) is OMITTED upstream from
asimplied.csv. It is not a regularly scheduled service and the source lists neither a
Ground Handler (GHA) nor a Capacity (cap) for it, so it cannot contribute passengers.
The original schedule including it is preserved at asimplied_with_B4_443_raw.csv.

Author: Yash Moitra, Delhi International Airport Limited.
"""
import csv
from datetime import datetime

SRC = "asimplied.csv"
OUT = "seats.csv"

def parse_sobt(s):
    # source format e.g. "21-06-2026 0:05"
    return datetime.strptime(s.strip(), "%d-%m-%Y %H:%M")

# 1. read flights (source is already cleaned: no blank cap / GHA)
flights = []
with open(SRC, encoding="latin1", newline="") as fh:
    for r in csv.DictReader(fh):
        if r["Seats"].strip() == "":
            raise ValueError(f"Blank cap for {r['Flight Designator']} - clean source first")
        cap = int(r["Seats"])
        if cap <= 0:
            raise ValueError(f"Non-positive cap for {r['Flight Designator']}")
        dt = parse_sobt(r["SOBT"])
        flights.append({
            "n": int(r["S.no"]),
            "flight": r["Flight Designator"].strip(),
            "route": r["Routing"].strip(),
            "dest": r["dest_iata"].strip(),
            "dep": dt.strftime("%H%M"),       # HHMM, 0000..2359
            "cap": cap,
            "dep_dt": dt,
        })

# 2. order by n (the canonical serial, which follows dep in the source)
flights.sort(key=lambda f: f["n"])

# 3. integrity checks on the flight set
n_last = len(flights)
ns = [f["n"] for f in flights]
assert ns == list(range(1, n_last + 1)), "n is not contiguous 1..n_last"
for a, b in zip(flights, flights[1:]):
    assert a["dep_dt"] <= b["dep_dt"], f"dep order breaks at n {a['n']}->{b['n']}"

# 4. enumerate passengers (many-to-one assignment pax -> n)
N = sum(f["cap"] for f in flights)
rows = []
pax = 0
for f in flights:
    for j in range(1, f["cap"] + 1):
        pax += 1
        rows.append([pax, f["n"], f["flight"], f["route"], f["dest"], f["dep"], f["cap"], j])
assert pax == N

# 5. write output
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["seat", "n", "flight", "route", "dest", "dep", "cap", "seat_on_flight"])
    w.writerows(rows)

# 6. report
print(f"flights n_last = {n_last}")
print(f"passengers N   = {N}")
print(f"first pax row  = {rows[0]}")
print(f"last  pax row  = {rows[-1]}")
print(f"wrote {OUT}")
