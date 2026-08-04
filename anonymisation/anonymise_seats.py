#!/usr/bin/env python3
"""
Checks-in, and Balances: a Matter of Time
Anonymisation of the seat universe to a hypothetical airport.

Author: Yash Moitra
Institution: Delhi International Airport Limited
Date: August 04, 2026

WHAT THIS DOES
    Reads the seat universe seats.csv and writes seats_anonymised.csv, applying
    exactly the alias map that anonymise_schedule.py applies to the schedule:

        flight    real designator becomes its alias, so 'Airline37 18'
        route     each segment aliased, so 'VMT-ABC-XYZ'
        dest      the destination airport alias

    seat, n, dep, cap and seat_on_flight are carried through unchanged. There is
    no date anywhere in this file: dep is a bare HHMM clock time, so the
    DD/MM/YYYY placeholder treatment applied to the schedule does not arise here.

WHY IT IMPORTS RATHER THAN REBUILDS
    The maps come from anonymise_schedule.build_maps, called on the same master
    schedule. Nothing is re-derived and nothing is read from the crosswalk, so
    seats_anonymised.csv cannot drift out of agreement with
    asimplied_anonymised.csv. Run either script in either order and the two
    files still join on flight, route and dest.

USAGE
    python3 anonymise_seats.py [path/to/seats.csv]
"""
import csv
import os
import sys

import anonymise_schedule as sched

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, os.pardir, "seats.csv")
OUT = os.path.join(HERE, "seats_anonymised.csv")


def main():
    schedule = sched.load_master()
    m = sched.build_maps(schedule)
    airport_map, designator_map = m["airport"], m["designator"]

    with open(SRC, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    fields = list(rows[0].keys())

    out = []
    for r in rows:
        o = dict(r)
        o["flight"] = designator_map[r["flight"].strip()]
        o["route"] = sched.alias_route(r["route"], airport_map)
        o["dest"] = airport_map[r["dest"].strip()]
        out.append(o)

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(out)

    print(f"seed              : {sched.SEED}")
    print(f"seats             : {len(out)}")
    print(f"flights covered   : {len({r['flight'] for r in out})}")
    print(f"columns unchanged : seat, n, dep, cap, seat_on_flight")
    print(f"columns aliased   : flight, route, dest")
    print(f"wrote {os.path.basename(OUT)}")


if __name__ == "__main__":
    main()
