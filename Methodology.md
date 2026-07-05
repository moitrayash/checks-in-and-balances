# Pax Forecast Model: Methodology

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** June 19, 2026

This document records, step by step, how the model is built: objective, inputs,
assumptions, procedure, decisions and their rationale, data treatments and gaps, outputs,
and verification (Ground Rule 5). Variables follow `Variable_Names.md`; terms follow
`Definitions.md`. Exhibits are captioned and numbered by class (Ground Rule 3).

## Exhibit index

Assumptions: 1 one passenger per seat, 2 existence tail rule, 3 homogeneous service, 4
rational counter choice. Constraint (1) desk operating window. Equations (1) universe
size, (2) existence, (3) entry-time distribution, (4) service rate, (5) wait at a desk,
(6) chosen wait. Tables 1 seats schema, 2 universe summary, 3 loyalty tiers, 4 cabin
classes, 5 OMDA targets. Figures: M1 entry-time distributions, one per flight
(`curves.Rmd`, rendered `curves.pdf`). The seat-level master is `seats.csv`; the
seat-level master with entry-time model columns is `seats.xlsx`.

## Step 1 - Construct the seat universe (complete)

**Objective.** Enumerate every occupiable seat implied by the foundation schedule and assign
each to exactly one flight (a many-to-one assignment), producing the seat-level master
`seats.csv`.

**Inputs.** `asimplied.csv`, the foundation schedule. Columns map to canonical variables:
S.no to `n`, Flight Designator to `flight`, Routing to `route`, dest_iata to `dest`, SOBT
to `dep`, Seats to `cap`.

**Data Note (B4 443 omission).** Flight B4 443 (Beond, DEL-MLE, scheduled 17:55) is omitted
from the analysis. It is not a regularly scheduled service and the source lists neither a
Ground Handler nor a Capacity for it; with no `cap` it cannot contribute seats and with no
GHA it cannot be assigned handling. (Airline spelling may differ across sources.) The
original schedule including it is preserved at `asimplied_with_B4_443_raw.csv`; after removal
the flight serial `n` was re-sequenced to remain contiguous 1 to 164.

**Ground-handling Note.** AIESL (Air India Engineering Services Ltd) is treated as a Ground
Handler independent of, and not merged with, AISATS. The cleaned schedule carries AISATS
(83 flights), BFS (71), Ramp 360 (9), and AIESL (1).

**Assumption 1.** *One seat serial per occupiable seat. Each offered seat receives one
serial; the seat universe is built at full occupancy. Realistic load factors and no-shows
are applied in Step 2 and are out of scope here.*

**Equation (1) - Universe size.** N = sum over n from 1 to n_last of cap(n), with n_last =
164 and N = 39,610.

**Assignment.** Seats are enumerated flight by flight in `dep` order: seat 1 is the first
seat of n = 1 and seat N is the last seat of n = n_last. The map `seat` to `n` is
many-to-one.

**Procedure.** `build_passengers.py` reads `asimplied.csv`, sorts flights by `dep` (serial
`n`), checks that `n` is contiguous and that `dep` is non-decreasing, then emits one row
per seat.

**Output, Table 1 (seats.csv schema).** Columns: `seat`, `n`, `flight`, `route`, `dest`,
`dep`, `cap`, `seat_on_flight`.

**Output, Table 2 (universe summary).** n_last = 164 flights; N = 39,610 seats; first =
(seat 1, n 1, AI 173, dep 0005); last = (seat 39,610, n 164, UA 083, dep 2335).

**Verification.** Row count = 39,610; `seat` contiguous and unique 1 to N; each `seat` mapped
to exactly one flight; per-flight seat count equals `cap` for all 164 flights; sum of `cap`
cross-checked against the source; all `dep` valid HHMM; and checkinopen = dep minus 4h,
checkinclose = dep minus 1h confirmed for every flight (this anchors Constraint (1)).

## Step 2 - Existence and entry times (specified; build pending design confirmation)

**Objective.** Overlay realised demand on the seat universe and assign each realised
passenger a time of entry to the check-in area.

**Assumption 2.** *Existence tail rule. For each flight, the lowest-indexed round(LF times
cap) seats are realised (exists = 1) and the remaining top (1 minus LF) times cap are not
(exists = 0); unoccupied seats carry no entry time.*

**Equation (2) - Existence.** exists(seat) = 1 if seat_on_flight is at most round(LF times
cap); the realised passenger count is `pax` = round(LF times cap). Total realised demand
therefore varies with LF.

**Equation (3) - Entry-time distribution.** For an occupied seat (a `pax`) on a flight,
entry(pax) follows F_m(. given flight), where each model m is a distribution over the
flight's check-in window [dep minus 0400, dep minus 0100]. Different models redistribute
entry times; the realised passenger count is set by LF (Equation (2)).

**Build note (entry-time models instantiated).** The model layer is stored as columns in
`seats.xlsx`, one column per entry-time model, one value per seat, in minutes before
departure. Thirteen Normal models are populated: M1 (mean 150, SD 30), M2 (165, 30), M3
(150, 60), M4 (120, 15), M5 (120, 30), M6 (120, 45), M7 (120, 60), M8 (150, 15), M9 (150,
45), M10 (180, 15), M11 (180, 30), M12 (180, 45), M13 (180, 60); all at LF = 1 for now. The
first model M1 is visualised per flight in `curves.Rmd` (rendered `curves.pdf`): one Normal
density per flight over clock time, centred at the mean entry time mu = dep minus 150
minutes, SD 30 minutes, with a dashed line marking mu, one flight per page in departure
order. The vertical axis is expected pax per 10-minute interval; with LF = 1 the area under
each curve equals the flight `cap`.

**Build update (June 23, 2026).** The model layer has since been expanded from the
thirteen Normal models to a catalogue of 104 entry-time models, stored one column per
model in `seats.xlsx` (sheet `seats`, with a `reference` tab): Normal N1 to N13, Uniform
U1, Exponential Growth EG0 to EG5, Exponential Decay ED0 to ED5, Skew-Left SL1 to SL39,
and Skew-Right SR1 to SR39. Full closed-form definitions and parameters are catalogued in
`model_equations.md` (densities restated in `model_equations_filled.md`), and every model
is verified against its target moments in `verification_report.csv` (104 of 104 PASS).
Per-model renders (entry-time curves, comparison curves, and stacked airline and GHA
views, plain and coloured) are in `0623.2203 renderings/`, ten files per model.

**Build update (June 30, 2026).** Steps 3 and 4 have been carried substantially further in
`assumed statics/`: a verified FIFO wait engine (Equations (7) to (14)), counter-capacity
and time-varying allocation rules (Equations (15) and (16)), two service regimes (r200 =
200 s per passenger, r180 = 180 s), two wait targets (20 and 40 minutes), three pooling
granularities (per flight, per airline, per GHA), and a comparison against the physical
supply of 168 counters across 13 islands. See
`assumed statics/Methodology_Counter_Allocation.md`, which continues the Equation
sequence of this document.

**Open decisions (Step 2).** Per-flight or per-segment load factors (currently LF = 1);
choice among M1 to M13 (or a blend) for downstream queueing; the existence overlay
(Equation (2)) and entry-to-arrival timing. See "Open design decisions".

## Step 3 - Check-in desks and service (specified)

**Objective.** Represent the supply side: open check-in desks per airline over time, each
serving passengers at a processing speed.

**Constraint (1) - Desk operating window.** Desks for a flight may be open only within [dep
minus 0400, dep minus 0100]; they cannot open earlier or stay open later. Verified to
coincide with [checkinopen, checkinclose] in the data.

At any time `t`, airline `a` has `D(a, t)` desks open; `D` may change over time. Each desk
`k` is a point with a processing speed.

**Processing speed.** Service time `tau` is in seconds per passenger; equivalently a service
rate `mu` per unit time.

**Equation (4) - Service rate.** mu = 1 / tau.

**Assumption 3.** *Homogeneous service. All desks (points) are equal in processing speed and
capacity for now; this will be made idiosyncratic over airline and over GHA in a later
revision.*

## Step 4 - Eligibility and wait time (specified)

**Objective.** Determine which desks a passenger may use and the wait they endure, against
the OMDA service benchmark.

Desk eligibility `E(p)`, which desks in the open set a passenger may access, depends on
passenger attributes: `loyaltystatus` (Table 3), `class` (Table 4), and in some cases
`fastforward`. The access mapping is to be formalised.

**Table 3 (loyalty tiers).** 0 none, 1 silver, 2 gold, 3 platinum, 4 1K-equivalent, 5
GS-equivalent.

**Table 4 (cabin classes).** 1 economy, 2 premium economy, 3 business, 4 first.

**Equation (5) - Wait at a desk.** For a passenger arriving at desk k, w_{p,k} = (L_k times
tau) minus e_k, where L_k is the number of passengers ahead (in queue plus the one in
service) and e_k is the time already elapsed on the passenger currently in service.

**Assumption 4.** *Rational counter choice. A passenger joins the eligible open desk offering
the least wait; the wait is computed for every eligible desk.*

**Equation (6) - Chosen wait.** w_p = min over k in E(p) of w_{p,k}, attained at desk k*_p =
argmin.

**Table 5 (OMDA targets).** Ideal wait at most 5 min for any business-class passenger; at
most 20 min for any economy passenger. Benchmark only; not a model input.

## Open design decisions

(i) Model-layer storage: long tidy table (seat by model by LF), a parametric generator
(parameters plus seed), one wide column per model, or a file per scenario. (ii) Entry-time
source: reuse the existing T3 check-in model (`pre0618/T3 Checkin Model/dial_t3_checkin_model.Rmd`)
and `Pax Arrival Times.xlsx`, a uniform draw over the check-in window, a peaked parametric
form, or several to compare. (iii) Load factor: single global value (default 0.90) versus
per-flight or per-segment, and the scenario set to sweep. (iv) Desk supply `D(a, t)`: source
or estimate of how many desks each airline opens over time. (v) Eligibility mapping `E(p)`:
the precise desk-access rule by `class`, `loyaltystatus`, and `fastforward`.

## Environment and housekeeping notes

`seats.csv` is rebuilt from the cleaned schedule by `build_passengers.py`. The R/knitr
renders of `flight_table` predate the B4 443 removal and should be re-knit from
`flight_table.Rmd` to refresh them. B4 443 is gone from the source and all data outputs.
