# Pax Forecast Model: Total Rundown

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** June 19, 2026

This is the model overview required as a total rundown, written in line with the ground
rules: it uses the variable list (`Variable_Names.md`) and definitions list
(`Definitions.md`), refers to assumptions, equations, constraints and tables by their
captioned numbers (maintained in `Methodology.md`), and is authored and dated per Ground
Rule 4.

## Purpose and scope

The model forecasts the build-up of departing passengers at check-in so that wait times can
be estimated and tested against service targets. The scope is a single operating day, Day 7
(21 June 2026), of international departures from Delhi (DEL) Terminal 3. After cleaning, the
schedule contains 164 flights and a maximal 39,610 seats (N, Equation (1)).

The model is built in layers: a fixed schedule foundation, a seat universe with a
load-factor-driven existence overlay, a set of entry-time models, a check-in desk and
service representation, and a queue and wait computation assessed against the OMDA
benchmark.

## Schedule foundation (Layer A)

The foundation schedule `asimplied.csv` holds one row per flight, each described by the core
author-defined variables: `flight`, `n`, `route`, `dest`, `cap`, and `dep`. The serial `n`
runs 1 to n_last (= 164) in departure order. One flight, B4 443 (Beond, DEL-MLE), is omitted
because the source gives it neither a Ground Handler nor a Capacity (Methodology, Data Note);
the original is preserved as `asimplied_with_B4_443_raw.csv`. AIESL is treated as a Ground
Handler independent of AISATS.

## Seats and existence (Layer B)

Step 1 enumerates the universe: one occupiable seat per physical seat, assigned many-to-one
to its flight, indexed `seat` = 1 to N in departure order (Assumption 1, Equation (1)). The
result is the seat-level master `seats.csv` (Table 1), with 39,610 rows (Table 2).

Real demand is then thinned by a load factor. Under Assumption 2 and Equation (2), each
flight realises round(LF times cap) passengers (`pax`), its lowest-indexed seats, and the
rest are marked exists = 0. Because LF is a free parameter (for example 0.90), the realised
passenger count is deliberately variable across scenarios; unoccupied seats never enter the
system.

## Entry-time models (Layer C)

Every occupied seat (a `pax`) is assigned an entry time, the moment they enter the check-in
area, drawn from a model m, which is a distribution over the flight's check-in window [dep
minus 4h, dep minus 1h] (Equation (3)). Several models can coexist (M1, M2, ...), each
distributing entry times differently; unoccupied seats have no entry time. This layer is
where the bulk of modelling judgement lives, and is the natural place to use the existing T3
check-in work (`pre0618/T3 Checkin Model`, `Pax Arrival Times.xlsx`).

## Check-in desks and service (Layer D)

On the supply side, each airline `a` opens `D(a, t)` check-in desks at time `t`, and `D` may
change through the day. Desks may be open only within [dep minus 4h, dep minus 1h]
(Constraint (1)), which the data confirms equals [checkinopen, checkinclose] for every
flight. Each desk `k` is a point with processing speed `tau` (seconds per passenger), or
rate `mu` = 1 / tau (Equation (4)). For now all desks share the same speed and capacity
(Assumption 3); this homogeneity will later be made idiosyncratic by airline and by GHA.

## Eligibility, queueing and wait (Layer E)

Not every passenger may use every desk. The eligible set `E(p)` is governed by the passenger
attributes `loyaltystatus` (Table 3), `class` (Table 4), and `fastforward`. At a given desk
the wait is the work still ahead: passengers ahead times service time, less the time already
spent on the passenger in service (Equation (5)). A rational passenger joins the eligible
desk with the least wait (Assumption 4, Equation (6)). The resulting waits are judged against
the OMDA Target (Table 5): at most 5 minutes for business class, at most 20 minutes for
economy.

## Variables, assumptions and equations

The full variable registry is in `Variable_Names.md` and all terms in `Definitions.md`. The
model rests on four assumptions (1 one passenger per seat, 2 the existence tail rule, 3
homogeneous service, 4 rational counter choice) and one operating constraint (1) on the desk
window. Its quantitative spine is Equations (1) to (6): universe size, existence, entry-time
distribution, service rate, wait at a desk, and chosen wait. All are catalogued in
`Methodology.md`.

## Artifacts

`asimplied.csv` (cleaned foundation schedule, 164 flights); `seats.csv` (seat-level
master, 39,610 rows, Table 1); `seats.xlsx` (seat-level master with entry-time model
columns M1 to M13); `build_passengers.py` (reproducible Step-1 build);
`asimplied_with_B4_443_raw.csv` (provenance); `flight_table.Rmd` (rendered schedule view);
`curves.Rmd` (rendered `curves.pdf`: M1 entry-time distribution per flight, one per page);
and the governance set `00_Ground_Rules.md`, `Variable_Names.md`, `Definitions.md`,
`Methodology.md`, and this `Model_Overview.md`.

## Status

Built and verified: Layers A and B (schedule foundation and seat universe, Step 1); Layer
C entry-time models (Step 2 build note: 104 models, N1 to SR39, instantiated in
`seats.xlsx` and verified in `verification_report.csv`); and, in `assumed statics/`, the
Layer D and E wait engine and counter allocation (Equations (7) to (16)): FIFO waits,
per-minute staffing profiles, two service regimes (180 s and 200 s per passenger), two
targets (20 and 40 minutes), three pooling granularities, and the comparison against the
physical supply of 168 counters (headline: at 180 s per passenger the 20-minute OMDA
target fits within 168 counters under every pooling; arrival shape, not counter count,
governs feasibility).

Still open, as listed in `Methodology.md` and
`assumed statics/Methodology_Counter_Allocation.md`: load-factor scenarios below 1, desk
eligibility by class and loyalty (the mapping `E(p)`), island and 14-per-island supply
constraints, and the tighter time-varying optimum.
