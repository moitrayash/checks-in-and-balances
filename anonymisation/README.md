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
| `anonymisation_crosswalk.csv` | The reverse map, real value to alias, 403 rows. Withhold from any public release. |
| `anonymise_schedule.py` | The transform. Run it to regenerate both files from the master. |
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
| Flight numbers (`Flight Designator`) | Renumbered `01` upward inside each airline, so `Airline47 13` |
| Dates (`SOBT`, `checkinopen`, `checkinclose`) | The literal placeholder `DD-MM-YYYY`, or `DD-1-MM-YYYY` where the timestamp falls on the day before departure |
| `Public Terminal` | Column dropped. It read `Terminal 3` on all 164 rows and carried no variance. |

Seats, clock times, traffic type, `S.no`, column order and row order are carried
through untouched.

The date placeholder keeps its day offset because 33 check-in windows open, and 9
close, on the evening before departure. Flattening every timestamp to a single
`DD-MM-YYYY` would make a counter opening at 20:05 the previous evening
indistinguishable from one opening at 20:05 on the day itself, and the FIFO wait
engine orders on that distinction.

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
python3 anonymise_schedule.py            # regenerates the CSV and the crosswalk
node verify_reproducibility.js           # prints the same map, independently derived
```

The script reads `excluded_iata_codes.txt` rather than querying an airport
database at run time, so a future change in any upstream dataset cannot silently
shift the map.

## Verification performed

Twenty-six checks pass on the current output: row and seat totals preserved
(164 and 39,610), the dropped column absent and all others in their original
order, every alias family a strict one to one mapping, no alias colliding with
any of the 7,884 live IATA codes, aliases spread across 25 distinct first
letters, day offsets and clock times preserved on all 492 timestamps, and a leak
test confirming that none of the 461 real identifier strings appears anywhere in
the output. The JavaScript reimplementation reproduces all 403 aliases exactly.

## Note on the crosswalk

`anonymisation_crosswalk.csv` reverses the anonymisation completely. It is
carried here deliberately, on the understanding that this repository becomes
private and that a separate public repository will carry the anonymised
artefacts alone. The crosswalk must not travel into that public repository, and
because git history is permanent, it should never be committed there even once.
