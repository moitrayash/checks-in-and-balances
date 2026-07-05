# Pax Forecast Model - Definitions List

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** June 19, 2026

Living registry per Ground Rule 2. Updated as relevant as the model is built.

## Schedule, seats & passengers

| Term | Definition |
|---|---|
| **Foundation schedule** | The canonical one-row-per-flight departure schedule for the operating day, held in `asimplied.csv` (164 flights after the B4 443 omission). The input to Step 1. |
| **Corpus** | The cleaned schedule table of the six author-defined variables (`flight`, `n`, `route`, `dest`, `cap`, `dep`), one row per flight ordered by `n`. Held as the `corpus` tab of `asimplied.xlsx`. |
| **Seat** | The seat serial (variable `seat`): one per occupiable seat, continuous over all flights in departure order. The seat-level master is `seats.csv`. |
| **Seat universe** | The maximal set of occupiable seats, one per seat, of size `N` = Σ `cap`. A passenger is an occupied seat; the realised count per flight is round(`LF` × `cap`). |
| **Passenger (`pax`)** | A realised passenger: an occupied seat (`exists` = 1). Per-flight count `pax` = round(`LF` × `cap`). |
| **Operating day ("Day 7")** | The single schedule day modelled: 21-06-2026. All `dep` times fall within this day. |
| **SOBT** | Scheduled Off-Block Time - the scheduled time a flight pushes back from its stand. Used as the variable `dep`. |
| **Flight designator** | Carrier code plus flight number identifying a scheduled service (variable `flight`). |
| **Route / Routing** | The ordered sequence of airports for a service, origin DEL (variable `route`). |
| **Destination** | The final airport of the route (variable `dest`, 3-letter IATA). |
| **IATA code** | Three-letter airport identifier (e.g. DEL, SFO). |
| **Capacity** | Number of seats offered on a flight (variable `cap`). |
| **Many-to-one assignment** | A mapping in which each seat is assigned to exactly one flight while a flight carries many seats. |
| **B4 443 omission** | Flight B4 443 (Beond, DEL-MLE) is excluded from the analysis: it is not a regularly scheduled service and the source lists neither a Ground Handler nor a Capacity for it. See Methodology, Data Note. |

## Load, existence & entry

| Term | Definition |
|---|---|
| **Load factor (`LF`)** | Assumed fraction of seats occupied; realised passengers per flight = round(`LF` × `cap`). Varied across scenarios (e.g. 0.90). |
| **Existence (`exists`)** | `exists(seat)` ∈ {0, 1}: 1 if a seat is occupied (a `pax`), else 0. Unoccupied seats have no entry time. |
| **Check-in window** | Opens at `dep` - 0400 (four hours before departure) and closes at `dep` - 0100 (one hour before). Equals [`checkinopen`, `checkinclose`] in the data. |
| **Entry time** | `entry(pax)`: the time at which a passenger (`pax`) enters the check-in area; defined for each `pax`. |
| **Entry-time model (`m`)** | A distribution function over entry times. Different models distribute `entry(pax)` in different ways; passenger counts vary with `LF`. |

## Ground handling

| Term | Definition |
|---|---|
| **GHA (Ground Handling Agent)** | The agent providing ground/check-in handling for a flight. Values in the schedule: AISATS, BFS, Ramp 360, AIESL. |
| **AISATS** | AI-SATS, a ground-handling joint venture. Treated as a distinct GHA. |
| **AIESL** | Air India Engineering Services Ltd - treated as a Ground Handler **independent of and not merged with AISATS**. |

## Check-in desks, service & queueing

| Term | Definition |
|---|---|
| **Check-in desk ("point")** | A single check-in position (variable `k`). An airline has `D(a, t)` desks open at time `t`; this can change over time. |
| **Desk operating window** | Constraint that desks for a flight may be open only within [`dep` - 0400, `dep` - 0100]. In the data this equals [`checkinopen`, `checkinclose`] for every flight. |
| **Processing speed** | Service time per passenger, `tau` (seconds per pax), or equivalently a service rate `mu` = 1/`tau` (pax per unit time). |
| **Eligibility (`E(p)`)** | The set of desks a passenger may use, determined by `class`, `loyaltystatus`, and `fastforward`. (Mapping to be formalised.) |
| **`loyaltystatus`** | Loyalty tier 0-5: none, silver, gold, platinum, 1K-equivalent, GS-equivalent. |
| **`class`** | Cabin class 1-4: economy, premium economy, business, first. |
| **`fastforward`** | Binary {0,1}: whether a passenger has purchased queue priority (e.g. IndiGo). |
| **Wait time (`w`)** | Time a passenger waits before service begins. For a single eligible desk: (passengers ahead) × `tau` minus time already elapsed on the passenger currently in service. With several eligible desks, the passenger is assumed to choose the desk with least wait. |
| **Rational counter choice** | Assumption that a passenger joins the eligible open desk offering the least wait time. |
| **OMDA Target** | Benchmark service level the model should ideally meet: ≤ 5 min wait for any business-class passenger and ≤ 20 min for any economy passenger. (Sidenote / benchmark, not a model input.) |
