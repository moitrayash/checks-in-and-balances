# Checks-in, and Balances: a Matter of Time - Data Dictionary

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** July 05, 2026

Column-by-column description of every data file in the repository. Variables follow
`Variable_Names.md`; terms follow `Definitions.md`. Times of day are HHMM (24 h) unless
stated; "minutes before departure" is the entry-time convention of Equation (3); clock
minutes follow Equation (7), where negative values fall on the evening of June 20, 2026.

## Root data files

### asimplied.csv (foundation schedule; 164 rows, one per flight)

| Column | Meaning |
|---|---|
| `S.no` | Flight serial `n`, 1 to 164, contiguous in departure order |
| `Airline code` | Two-character carrier code (IATA), e.g. AI |
| `Flight Designator` | Carrier code plus flight number (`flight`), e.g. AI 173 |
| `SOBT` | Scheduled Off-Block Time, `DD-MM-YYYY H:MM`; the variable `dep` |
| `checkinopen` | Check-in opening, `dep` minus 4 h (verified for every flight) |
| `checkinclose` | Check-in closing, `dep` minus 1 h (verified for every flight) |
| `Routing` | Ordered IATA airports, origin DEL (`route`) |
| `Traffic Type` | INTERNATIONAL for all rows |
| `Public Terminal` | Terminal 3 for all rows |
| `GHA` | Ground Handling Agent: AISATS, BFS, Ramp 360, or AIESL |
| `Seats` | Capacity `cap`, seats offered |
| `dest_iata`, `dest_city`, `dest_country` | Final destination (`dest`) and its city and country |
| `airline_name`, `airline_country` | Operating carrier's name and home country |

### asrecd.csv (schedule as received; 165 rows)

The uncleaned source. Columns: `DATE`, `Airline code`, `Flight Designator`, `SOBT` (time
only), `Hour`, `Routing`, `Traffic Type`, `Public Terminal`, `GHA`, `Seats`. Includes
flight B4 443 with blank GHA and Seats; excludes the enrichment columns of
`asimplied.csv`.

### asimplied_with_B4_443_raw.csv (provenance backup; 165 rows)

`asimplied.csv` exactly as it stood before the B4 443 removal and re-serialisation.

### seats.csv (seat-level master; 39,610 rows, one per occupiable seat)

| Column | Meaning |
|---|---|
| `seat` | Seat serial, 1 to N = 39,610, continuous over all flights in departure order |
| `n` | Flight serial of the seat's flight |
| `flight`, `route`, `dest`, `dep`, `cap` | Copied from the flight (see above); `dep` as HHMM |
| `seat_on_flight` | Seat ordinal within the flight, 1 to `cap` |

### seats.xlsx (seat-level master plus the model layer; sheets `seats`, `reference`)

Sheet `seats`: rows 1 to 9 are a header block (row 1 a note; rows 2 to 9 the per-model
metadata: Family, Distribution, Target mean, Target SD, Skew alpha, Exp scale s, Exp
lambda, Seed). Row 10 holds column names; data start at row 11. Columns A to H are
`seats.csv` verbatim; the following 104 columns, N1 to N13, U1, EG0 to EG5, ED0 to ED5,
SL1 to SL39, SR1 to SR39, hold that model's entry time for the seat, in integer minutes
before departure at LF = 1 (negative = after midnight relative to departure; Uniform and
Exponential families live on the window [0, 240]). Sheet `reference` restates the model
catalogue. Definitions and seeds: `model_equations.md`. In the Git repository this file is carried as split binary parts; run `python3 rejoin_seats.py` to reconstruct and verify it.

### model_equations.md / model_equations_filled.md

The 104-model catalogue: family, density, parameters, and seed per model; the `_filled`
variant restates every density with parameters substituted, ready to transcribe.

### verification_report.csv (104 rows, one per model)

| Column | Meaning |
|---|---|
| `Code`, `Family` | Model label (N1 to SR39) and family |
| `mean`, `SD`, `alpha`, `exp_s`, `seed` | Target parameters and seed, as applicable |
| `verdict`, `exact_match`, `mismatches` | PASS if the stored column reproduces the seeded draw exactly |
| `realized_mean`, `realized_SD`, `realized_skew` | Moments realised over the 39,610 draws |
| `min`, `max`, `neg_count` | Range of entry minutes and count of after-midnight values |

## assumed statics/ (wait engine and counter allocation)

### counters_by_row.csv (13 rows)

`row` (island letter, A to N without I) and `counters` (physical counters on the island).
Total 168.

### waits_summary.csv (624 rows = 104 models x 3 groupings x 2 regimes)

Realised FIFO waits when each group (flight, airline, or GHA) operates a **single pooled
counter**, the do-nothing baseline that motivates allocation. Columns: `grouping`,
`model`, `regime` (r200 = 200 s per pax, r180 = 180 s), `N` (39,610), `mean_wait`,
`median_wait`, `p90_wait`, `p95_wait`, `max_wait` (minutes), `pct_gt5`, `pct_gt20`,
`pct_gt60` (share of passengers waiting beyond 5, 20, 60 minutes), `pct_finish_after_dep`
and `pct_finish_after_close` (share processed only after departure, or after the
check-in window closed).

### allocation_summary.csv / .xlsx (1,248 rows = 104 x 3 x 2 x 2 targets)

The Equation (16) time-varying allocation. Columns: `grouping`, `model`, `regime`,
`target_min` (20 or 40), `n_groups`, `airport_peak` (max over minutes of the summed desk
profile), `sum_group_peaks`, `max_single_group`, `total_counter_min` (counter-minutes
consumed), `supply` (168), `feasible_168` (True if `airport_peak` fits the supply).

### alloc_heuristic_{flight,airline,gha}.csv

The same computation as `allocation_summary.csv`, one file per grouping, without the
`supply` and `feasible_168` columns.

### alloc_exact_N1.csv (6 rows)

Constant staffing solved exactly for model N1: each group holds a fixed counter count all
day, the minimum that meets the target. Columns: `grouping`, `regime`, `target_min`,
`airport_peak_exact` (sum of the constant counts, the concurrent requirement),
`total_desks_exact`. This is the constant-staffing scheme referenced in Section XII of
the counter-allocation methodology (there named `alloc_constant_staffing_N1.csv`); the
figures confirm Section XI note 2, that constant staffing is materially less efficient
than the time-varying rule.

### profile_{flight,airline,gha}_N1.csv

Minute-by-minute airport-wide desk profile for model N1 under the respective pooling.
Columns: `clock_min` (Equation (7) clock, negatives on June 20 evening) and four desk
counts, `desks_W20_r200`, `desks_W20_r180`, `desks_W40_r200`, `desks_W40_r180`.

### schedule_{flight,airline,gha}_W{20,40}.csv.gz

The full minimum-counter desk schedules per group per minute produced by the Equation
(16) rule, gzip-compressed; one file per grouping and target, both regimes inside.

### worked_example.csv / .xlsx (288 rows)

Flight AI 173 under model N1, spot-verifiable by hand: `seat`, `flight`, `N1_entry`
(minutes before departure), then wait and processed times under both regimes and all
three poolings (`N1_{wait,proc}_{r200,r180}_{flight,airline,gha}`), in clock minutes.

### wait_time.py

Reference implementation of Equations (7) to (16) with a self-test (Equations (10), (11),
and (14) cross-checks and the Section IV worksheet correction). Restored July 05, 2026;
validated to exact agreement on all 288 rows of `worked_example.csv`, both regimes.

### desk_schedule_readable.xlsx / allocation_summary.xlsx / waits_summary.xlsx / worked_example.xlsx

Formatted spreadsheet versions of the corresponding CSVs.

## pre0618/ (archive)

Earlier working files preserved for provenance, including `Foundation Schedule.xlsx` (and
its rebuilt variant), `Pax Arrival Times.xlsx`, the `T3 Checkin Model/` prototype,
profile scripts, and photographs (`Photos-3-001.zip`). Superseded by the root data files.
