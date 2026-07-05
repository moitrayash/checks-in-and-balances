# Pax Forecast Model - Variable Name List

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** June 19, 2026

Living registry per Ground Rule 1. Updated as relevant as the model is built. Each
variable is a class with the domain shown. Attribute variables may be read as
functions of the flight serial `n` - e.g. `cap(n)`, `dep(n)`, `dest(n)`.

**Naming-collision notes.** `N` (total seats) and `n` (flight serial) are reserved. The
count of open check-in desks is therefore written `D` (not `N`), and a desk index is
written `k` (not `n`).

## Schedule, seats & passengers (Steps 1-2)

| Variable | Meaning | Class / Domain | Example | First defined |
|---|---|---|---|---|
| `flight` | Flight designator (carrier code + number) | String | `AI 101` | Step 1 |
| `n` | Flight serial number | Integer, 1 ≤ `n` ≤ `n_last` | `1` | Step 1 |
| `route` | Routing; ordered IATA codes, origin DEL | String `DEL-...-XYZ` | `DEL-CCU-SFO` | Step 1 |
| `dest` | Final destination | String, 3-letter IATA | `SFO` | Step 1 |
| `cap` | Capacity (seats offered) of a flight | Integer ≥ 1 | `288` | Step 1 |
| `dep` | Departure time (SOBT), time of day | HHMM, 24h; 0000 ≤ `dep` ≤ 2359 | `0005` | Step 1 |
| `seat` | Seat serial; one per occupiable seat, continuous over all flights in `dep` order | Integer, 1 ≤ `seat` ≤ `N` | `1` | Step 1 |
| `seat_on_flight` | Seat ordinal within a flight | Integer, 1 ≤ `seat_on_flight` ≤ `cap` | `1` | Step 1 |
| `N` | Total seats in the universe: `N` = Σ `cap(n)` | Integer | `39610` | Step 1 |
| `n_last` | Number of flights (last serial) | Integer | `164` | Step 1 |
| `LF` | Load factor - assumed fraction of seats occupied | Real, 0 < `LF` ≤ 1 | `0.90` | Step 2 |
| `pax` | Realised passenger (an occupied seat, `exists` = 1); per-flight count `pax` = round(`LF` × `cap`) | Integer ≥ 0 | `259` | Step 2 |
| `exists` | Whether a seat is occupied: `exists(seat)` ∈ {0, 1}; a `pax` is a seat with `exists` = 1 | Binary ∈ {0, 1} | `1` | Step 2 |
| `entry(pax)` | Time a passenger (`pax`) enters the check-in area; defined for each `pax` | Timestamp (24h; may fall on day before `dep`) | `20-06-2026 21:30` | Step 2 |
| `m` | Entry-time model label (a distribution over `entry(pax)`) | Categorical/index | `M1` | Step 2 |

## Service & queue layer (Steps 3-4)

| Variable | Meaning | Class / Domain | Example | First defined |
|---|---|---|---|---|
| `a` | Airline (carrier) operating a flight | Categorical (carrier code) | `AI` | Step 3 |
| `t` | Clock time within the operating window | Timestamp / minutes | `2230` | Step 3 |
| `D` | Open check-in desks for an airline at time `t`; `D = D(a, t)` | Integer ≥ 0 (reserved ≠ `N`) | `6` | Step 3 |
| `k` | Check-in desk ("point") index in the open set | Integer, 1 ≤ `k` ≤ `D` (reserved ≠ `n`) | `1` | Step 3 |
| `tau` (τ) | Service time / processing speed, seconds per pax | Real > 0 (sec·pax⁻¹) | `90` | Step 3 |
| `mu` (μ) | Service rate, pax per unit time; `μ = 1/τ` | Real > 0 (pax·time⁻¹) | `40/hr` | Step 3 |
| `loyaltystatus` | Passenger loyalty tier | Integer 0-5: none, silver, gold, platinum, 1K-eq, GS-eq | `3` | Step 3 |
| `class` | Cabin class | Integer 1-4: economy, premium economy, business, first | `1` | Step 3 |
| `fastforward` | Purchased queue priority (e.g. IndiGo) | Binary ∈ {0, 1} | `0` | Step 3 |
| `E(p)` | Eligible desks a passenger `p` may use (from `class`, `loyaltystatus`, `fastforward`) | Set ⊆ open desks of the flight's airline | `{1,2}` | Step 4 |
| `w` | Wait time endured before service begins | Real ≥ 0 (minutes/seconds) | `12 min` | Step 4 |

*Author-defined core variables:* `flight`, `n`, `route`, `dest`, `cap`, `dep`.
*Introduced in Step 1:* `seat`, `seat_on_flight`, `N`, `n_last`.
*Introduced for Step 2 (mechanism specified, build pending):* `LF`, `pax`, `exists`, `entry(pax)`, `m`.
*Introduced for Steps 3-4 (specification stage):* `a`, `t`, `D`, `k`, `tau`, `mu`, `loyaltystatus`, `class`, `fastforward`, `E(p)`, `w`.
