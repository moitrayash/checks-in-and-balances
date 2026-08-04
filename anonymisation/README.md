# Anonymisation

**Project:** Checks-in, and Balances: a Matter of Time
**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** August 04, 2026

This folder holds the anonymised duplicate of the master schedule and everything
needed to reproduce or reverse it. It exists so that the model can be published
academically against a hypothetical airport, at the request of the schedule
provider. Nothing outside this folder is modified: `../asimplied.csv` remains the
master source of truth and every downstream artefact still uses it.

## Contents

| File | What it is |
|---|---|
| `asimplied_anonymised.csv` | The anonymised duplicate of `../asimplied.csv`. 164 flights, 39,610 seats. |
| `seats_anonymised.csv` | The anonymised duplicate of `../seats.csv`. One row per occupiable seat, N = 39,610. |
| `anonymisation_crosswalk.csv` | The reverse map, real value to alias, 403 rows. Withhold from any public release. |
| `anonymise_schedule.py` | The schedule transform, and the single source of the alias map. Run it to regenerate the schedule and the crosswalk. |
| `anonymise_seats.py` | The seat universe transform. Imports the map from `anonymise_schedule.py` rather than rebuilding it. |
| `excluded_iata_codes.txt` | The 7,884 live IATA codes that an airport alias may not collide with. |
| `verify_reproducibility.js` | An independent reimplementation in JavaScript, used to demonstrate that the map does not depend on the language it was built in. |

## What is replaced

| Field | Treatment |
|---|---|
| Airports (`Routing`, `dest_iata`) | Three random letters that are not a live IATA code. The hub, which appears on all 164 routings, is `VMT`. |
| Airlines (`Airline code`, `airline_name`) | `Airline01` to `Airline57` |
| Ground handlers (`GHA`) | `GHA01` to `GHA04` |
| Cities (`dest_city`) | `City01` to `City63` |
| Countries (`dest_country`, `airline_country`) | `Country01` to `Country46`, one shared map across both columns |
| Flight numbers (`Flight Designator`) | Renumbered from `101` upward inside each airline, always three digits and never a leading zero, so `Airline37 118` |
| `Public Terminal` | Column dropped. It read `Terminal 3` on all 164 rows and carried no variance. |

Seats, traffic type, `S.no`, column order and row order are carried through
untouched.

## Dates are deliberately not anonymised

`SOBT`, `checkinopen` and `checkinclose` carry their real values, byte-identical
to the master. The operating day is 21 June 2026, and 33 check-in windows open
and 9 close on the evening of 20 June. The three columns therefore remain
ordinary timestamps that any date parser reads directly, and the FIFO wait engine
needs no change.

This is a deliberate narrowing of the anonymisation, not an oversight. The real
date combined with this exact profile of 164 flights and 39,610 seats is
matchable against published schedules by a determined reader, so the schedule is
anonymised as to who, not as to when. Any release should say so plainly rather
than imply a stronger guarantee than the data carries.

## How the map is drawn

Assignment uses one primitive, SHA-256, and nothing else. No language's random
number generator is involved, so the same seed yields the same map in Python, R,
JavaScript or Julia.

For a value `v` in family `f`, the sort key is

```
H(v) = SHA256( SEED | f | v )        as a lowercase hex string
```

Entities are ordered by `(H(v), v)` ascending, the raw value breaking any hash
tie, and indices are handed out `01`, `02`, `03` and so on in that order.

Airport aliases are drawn by rejection sampling on the same hash:

```
candidate(k) = base26( int( SHA256( SEED | airport | v | k )[0:8], 16 ) mod 17576 )
```

starting at `k = 0` and incrementing until the candidate is neither a live IATA
code nor already taken. The pool is 26^3 = 17,576 combinations, of which 7,884
are live codes, leaving 9,692 available for 69 airports.

Seed: `20260621`.

Because the assignment is a pure function of the seed, the family name and the
value, the alias order carries no signal about traffic volume, alphabetical
position or departure time. Recovering the real schedule from the anonymised one
requires the crosswalk.

## Rebuilding

```
python3 anonymise_schedule.py            # regenerates the schedule and the crosswalk
python3 anonymise_seats.py               # regenerates the seat universe
node verify_reproducibility.js           # prints the same map, independently derived
```

Order does not matter. `anonymise_seats.py` calls `anonymise_schedule.build_maps`
on the same master schedule rather than rebuilding a map of its own or reading
the crosswalk, so the two outputs cannot drift apart.

The script reads `excluded_iata_codes.txt` rather than querying an airport
database at run time, so a future change in any upstream dataset cannot silently
shift the map.

## The seat universe

`seats_anonymised.csv` carries one row per occupiable seat, N = 39,610, and
aliases only the three columns that name a real entity: `flight`, `route` and
`dest`. `seat`, `n`, `dep`, `cap` and `seat_on_flight` are carried through
untouched. `dep` is a bare HHMM clock time and no date column exists here at
all.

The file joins to `asimplied_anonymised.csv` exactly as `../seats.csv` joins to
`../asimplied.csv`: the 164 flight aliases match, `route` agrees with `Routing`
and `dest` with `dest_iata` on every flight, and the seat count per flight equals
both the schedule's `Seats` and the `cap` column.

## Verification performed

Twenty-two checks pass on the seat universe and eighteen on the schedule: row and seat totals preserved
(164 and 39,610), the dropped column absent and all others in their original
order, every alias family a strict one to one mapping, no alias colliding with
any of the 7,884 live IATA codes, aliases spread across 25 distinct first
letters, every designator number three digits with no leading zero and no flight
carrying its own real number, all three datetime columns byte-identical to the
master, and a leak test
confirming that none of the 459 real entity identifier strings appears anywhere
in the output. The JavaScript reimplementation reproduces all 403 aliases exactly. The seat universe is separately checked to join to the anonymised schedule on all 164 flights and to draw no alias of its own.

## A note on flight numbers

Numbers run `101` upward within each airline, so the busiest carrier occupies
`101` to `150`. Ten of those values coincide with a real flight number appearing
somewhere else in the source schedule. This is a coincidence of value and never
of identity: no flight carries its own real number, and knowing that an alias
`131` exists says nothing about the real flight that bore `131`, which maps
elsewhere. The count of flights per airline is preserved and is visible in the
highest number each airline reaches.

## Note on the crosswalk

`anonymisation_crosswalk.csv` reverses the anonymisation completely. It is
carried here deliberately, on the understanding that this repository becomes
private and that a separate public repository will carry the anonymised
artefacts alone. The crosswalk must not travel into that public repository, and
because git history is permanent, it should never be committed there even once.
