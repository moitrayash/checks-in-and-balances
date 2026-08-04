#!/usr/bin/env python3
"""
Checks-in, and Balances: a Matter of Time
Anonymisation of the master schedule to a hypothetical airport.

Author: Yash Moitra
Institution: Delhi International Airport Limited
Date: August 04, 2026

WHAT THIS DOES
    Reads the master schedule asimplied.csv and writes asimplied_anonymised.csv,
    in which every real identifier is replaced by an alias:

        airports          three random letters that are NOT a live IATA code
        airlines          Airline01 .. Airline57
        ground handlers   GHA01 .. GHA04
        cities            City01 .. City63
        countries         Country01 .. Country46
        flight numbers    renumbered 01 .. 50 within each airline
        Public Terminal   column dropped (it was Terminal 3 on all 164 rows)

    Seats, all three datetime columns, traffic type, column order and row
    order are unchanged.

REPRODUCIBILITY
    Assignment is language independent. It uses only SHA-256, string sorting and
    integer arithmetic, so R, JavaScript, Julia or Python all produce the same
    map from the same seed. Nothing depends on a language's PRNG.

    For each entity the sort key is

        H(entity) = SHA256( SEED | family | value )            as a hex string

    Entities are ordered by (H, value) ascending, and indices are handed out
    01, 02, 03 ... in that order. The value breaks any hash tie, so the order is
    total and deterministic.

    Airport aliases are drawn by rejection sampling on the same hash:

        candidate(k) = base26( int( SHA256( SEED|airport|value|k )[0:8], 16 ) )

    starting at k = 0 and incrementing until the candidate is neither a live
    IATA code nor already taken. Live codes are read from
    excluded_iata_codes.txt, which is shipped alongside this script so the run
    does not depend on the version of any airport database.

USAGE
    python3 anonymise_schedule.py [path/to/asimplied.csv]
"""
import csv
import hashlib
import os
import sys
from collections import OrderedDict

SEED = "20260621"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, os.pardir, "asimplied.csv")
OUT = os.path.join(HERE, "asimplied_anonymised.csv")
XWK = os.path.join(HERE, "anonymisation_crosswalk.csv")
EXCL = os.path.join(HERE, "excluded_iata_codes.txt")
DROP_COLUMNS = ["Public Terminal"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def H(*parts):
    """SHA-256 hex digest of the parts joined by a pipe. The one primitive."""
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()


def canonical_order(values, family):
    """Total, language independent ordering of a set of entity values."""
    return sorted(values, key=lambda v: (H(SEED, family, v), v))


def base26(n):
    """Integer to a three letter code, AAA .. ZZZ."""
    return "".join(ALPHABET[(n // 26 ** i) % 26] for i in (2, 1, 0))


def load_excluded():
    """Live IATA codes that an alias must never collide with."""
    if os.path.exists(EXCL):
        with open(EXCL, encoding="utf-8") as fh:
            return {ln.strip().upper() for ln in fh if ln.strip() and not ln.startswith("#")}
    import airportsdata                      # fallback if the list is absent
    return set(airportsdata.load("IATA"))


def assign_airports(reals, excluded):
    """Rejection sampling: a random three letter code that is not a live IATA code."""
    alias, taken = OrderedDict(), set()
    for real in canonical_order(reals, "airport"):
        k = 0
        while True:
            cand = base26(int(H(SEED, "airport", real, k)[:8], 16) % (26 ** 3))
            if cand not in excluded and cand not in taken:
                break
            k += 1
        alias[real] = cand
        taken.add(cand)
    return alias


def assign_indexed(reals, family, template):
    """Hand out 01, 02, 03 ... in canonical order."""
    return OrderedDict(
        (real, template.format(i))
        for i, real in enumerate(canonical_order(reals, family), start=1)
    )




def load_master(path=None):
    with open(path or SRC, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def build_maps(rows):
    """Every alias map, derived from the master schedule alone.

    This is the single source of the alias assignment. anonymise_seats.py
    imports it rather than rebuilding its own, so the seat universe and the
    schedule can never drift out of agreement.
    """
    airports = set()
    for r in rows:
        airports |= {s.strip() for s in r["Routing"].split("-")}
        airports.add(r["dest_iata"].strip())

    airline_map = assign_indexed({r["Airline code"].strip() for r in rows}, "airline", "Airline{:02d}")

    # flight numbers, renumbered inside each airline, same canonical ordering
    by_airline = {}
    for r in rows:
        by_airline.setdefault(r["Airline code"].strip(), []).append(r["Flight Designator"].strip())
    designator_map = {}
    for code in sorted(by_airline):
        for n, real in enumerate(canonical_order(by_airline[code], "flight"), start=1):
            designator_map[real] = f"{airline_map[code]} {n:02d}"

    code_to_name = {}
    for r in rows:
        code_to_name.setdefault(r["Airline code"].strip(), r["airline_name"].strip())

    return {
        "airport": assign_airports(airports, load_excluded()),
        "airline": airline_map,
        "gha": assign_indexed({r["GHA"].strip() for r in rows}, "gha", "GHA{:02d}"),
        "city": assign_indexed({r["dest_city"].strip() for r in rows}, "city", "City{:02d}"),
        "country": assign_indexed(
            {r["dest_country"].strip() for r in rows} | {r["airline_country"].strip() for r in rows},
            "country", "Country{:02d}"),
        "designator": designator_map,
        "hub": max(airports, key=lambda a: sum(a in r["Routing"] for r in rows)),
        "code_to_name": code_to_name,
    }


def alias_route(routing, airport_map):
    """'DEL-CCU-SFO' becomes 'VMT-ABC-XYZ', segment by segment."""
    return "-".join(airport_map[s.strip()] for s in routing.split("-"))


def main():
    rows = load_master()
    fields = [c for c in rows[0].keys() if c not in DROP_COLUMNS]

    m = build_maps(rows)
    airport_map, airline_map = m["airport"], m["airline"]
    gha_map, city_map, country_map = m["gha"], m["city"], m["country"]
    designator_map, hub, code_to_name = m["designator"], m["hub"], m["code_to_name"]
    excluded = load_excluded()

    out = []
    for r in rows:
        code = r["Airline code"].strip()
        o = {k: v for k, v in r.items() if k not in DROP_COLUMNS}
        o["Airline code"] = airline_map[code]
        o["airline_name"] = airline_map[code]
        o["Flight Designator"] = designator_map[r["Flight Designator"].strip()]
        o["Routing"] = alias_route(r["Routing"], airport_map)
        o["GHA"] = gha_map[r["GHA"].strip()]
        o["dest_iata"] = airport_map[r["dest_iata"].strip()]
        o["dest_city"] = city_map[r["dest_city"].strip()]
        o["dest_country"] = country_map[r["dest_country"].strip()]
        o["airline_country"] = country_map[r["airline_country"].strip()]
        out.append(o)

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(out)

    with open(XWK, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["entity_type", "real_value", "alias", "note"])
        for real, a in airport_map.items():
            w.writerow(["airport", real, a, "hub" if real == hub else ""])
        for real, a in airline_map.items():
            w.writerow(["airline_code", real, a, code_to_name[real]])
        for real, a in gha_map.items():
            w.writerow(["ground_handler", real, a, ""])
        for real, a in city_map.items():
            w.writerow(["city", real, a, ""])
        for real, a in country_map.items():
            w.writerow(["country", real, a, ""])
        for real, a in sorted(designator_map.items()):
            w.writerow(["flight_designator", real, a, ""])

    print(f"seed                 : {SEED}")
    print(f"excluded IATA codes  : {len(excluded)}")
    print(f"flights              : {len(out)}")
    print(f"airports             : {len(airport_map)} (hub {hub} -> {airport_map[hub]})")
    print(f"airlines             : {len(airline_map)}")
    print(f"ground handlers      : {len(gha_map)}")
    print(f"cities               : {len(city_map)}")
    print(f"countries            : {len(country_map)}")
    print(f"columns dropped      : {DROP_COLUMNS}")
    print(f"wrote {os.path.basename(OUT)} and {os.path.basename(XWK)}")


if __name__ == "__main__":
    main()
