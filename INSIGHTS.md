# Checks-in, and Balances: a Matter of Time - Insights

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** July 05, 2026

Findings computed from the built layers: the foundation schedule (`asimplied.csv`), the
seat universe (`seats.csv`), the 104-model entry-time layer (`seats.xlsx`), and the wait
and allocation results (`assumed statics/`). Every figure below is reproducible from the
named files; the interactive versions live in `dashboard/index.html`.

## 1. The operating day at a glance

Day 7, June 21, 2026, Terminal 3, international departures only: 164 flights, 39,610
seats, 57 airlines, 65 destinations in 45 countries, 4 ground handlers. Median flight
capacity is 232 seats (range 118 to 509).

The day is double-peaked in offered capacity. The midnight hour (00:00 to 00:59) is the
single heaviest, 2,507 seats across 9 departures, followed closely by the late-morning
bank (2,404 seats in the 11:00 hour; the 12:00 hour has the most departures, 11). The
quietest hour is 17:00, a single pair of departures totalling 350 seats. By flight count
the early morning (00:00 to 04:59: 43 flights) and late evening (21:00 to 23:59: 24
flights) frame the day.

## 2. Concentration

Ground handling: AISATS serves 83 flights (20,203 seats, 51.0 percent of capacity), BFS
71 flights (16,602 seats, 41.9 percent), Ramp 360 9 flights (2,403 seats), AIESL 1 flight
(402 seats). Two handlers therefore carry 93 percent of the day.

The largest single aircraft movements are the 509-seat departures; the top destinations
by offered seats and the airline league table are tabulated in the dashboard's Explorer
tab.

## 3. Where the counter requirement peaks

Under the reference behaviour N1 (arrivals centred 150 minutes before departure, SD 30)
with the 20-minute target at 180 seconds per passenger, the airport-wide desk requirement
peaks at 08:49 to 08:54, serving the late-morning departure bank: 159 counters pooled per
flight, 150 per airline, 143 per GHA, against a supply of 168. The midnight capacity peak
produces its check-in surge on the evening of June 20 (roughly 20:00 to 23:00), which the
supply absorbs more comfortably.

Pooling is worth real counters: at the peak minute, pooling by GHA rather than per flight
saves 16 counters (159 to 143), and over the whole day it saves about 10.4 percent of
counter-minutes (134,965 down to 120,871).

## 4. Feasibility across all 104 arrival behaviours

Per-flight pooling, 20-minute target, airport peak versus the 168-counter supply:

| Family | r180 feasible | r200 feasible |
|---|---|---|
| Normal (13) | 10 of 13 | 6 of 13 |
| Uniform (1) | 1 of 1 | 1 of 1 |
| Exp growth (6) | 4 of 6 | 3 of 6 |
| Exp decay (6) | 3 of 6 | 2 of 6 |
| Skew-left (39) | 30 of 39 | 18 of 39 |
| Skew-right (39) | 26 of 39 | 15 of 39 |
| **All (104)** | **74 of 104** | **45 of 104** |

The gentlest behaviours need as few as 136 counters (N7, the flattest Normal, mean 120 SD
60; the Uniform and the flatter exponentials sit at 137). The harshest need 227 to 229
(EG5 and ED5, the two most concentrated bursts, scale 10 minutes). Service speed matters
almost as much as shape: moving from 200 to 180 seconds per passenger rescues 29 of the
104 behaviours at per-flight pooling.

## 5. The cost of doing nothing

`waits_summary.csv` prices the baseline of a single pooled counter per group. Per flight
under N1 at r180 the mean wait is measured in hours; per GHA it is measured in days
(mean 25,378 minutes). The allocation layer exists because no constant, small counter
count survives this schedule: staffing must follow the arrival curve.

Constant staffing solved exactly (N1) needs 207 concurrent counters per-flight at r180
for the 20-minute target, versus 159 for the time-varying rule: holding counters flat all
day costs about 30 percent more peak supply (`alloc_exact_N1.csv`).

## 6. What governs feasibility

Ordering the levers by leverage on the 20-minute target: first arrival behaviour (peak
requirement spans 136 to 229 counters across shapes, a 68 percent swing), then service
speed (180 versus 200 seconds moves the per-flight peak by roughly 7 to 12 percent), then
pooling breadth (flight to GHA saves another 8 to 10 percent). Counter count is the least
powerful lever: within realistic supply, behaviour and speed decide the day.

## 7. Verification posture

All 104 entry-time models pass moment verification (`verification_report.csv`). The wait
engine's three formulations agree to machine precision on randomised sequences, and the
restored `wait_time.py` reproduces all 288 rows of the worked example exactly, both
regimes, all three poolings. Load factor 1 everywhere: every figure above is a
worst-case, full-occupancy reading, per Assumption 1.
