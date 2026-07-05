# 0623.2203 renderings

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** June 23, 2026

832 ready-to-knit R Markdown files: every entry-time density model (104) crossed with every
view (8). Each `.Rmd` defaults to knitting to PDF (Ground Rule 10) and reads `asimplied.csv`
(included here), so it is self-contained: open any file and knit.

## Codename scheme

Files are named `<MODELCODE>__<VIEW>.Rmd`. The full map is in `_manifest.csv`
(columns: file, model, kind, view, ymax).

**Views (8):**

| View code | Meaning |
|---|---|
| `curves` | Per-flight density, one flight per page (black) |
| `curves_col` | Per-flight, coloured by airline |
| `comp` | Composite overlay of all flights, 12 time windows (black) |
| `comp_col` | Composite overlay, coloured by airline |
| `stk_air` | Stacked by airline (same-airline flights summed), black |
| `stk_air_col` | Stacked by airline, coloured |
| `stk_gha` | Stacked by ground handler (GHA), black |
| `stk_gha_col` | Stacked by GHA, coloured |

**Models (104):** `N1`-`N13` (Normal), `U1` (Uniform), `EG0`-`EG5` (Exponential growth,
early-heavy), `ED0`-`ED5` (Exponential decay, last-minute-heavy), `SL1`-`SL39` (Skew-left),
`SR1`-`SR39` (Skew-right). `t` is minutes before departure; Normal and Skew support all real
`t`; Uniform and Exponential are truncated to `0 <= t <= 240`.

## Shared y-axis (across all 104 models)

As requested, the y-axis is shared so models are directly comparable:

- Per-flight and overlay views (`curves`, `curves_col`, `comp`, `comp_col`): **0 to 600** pax per 10 min.
- Stacked views (`stk_air`, `stk_air_col`, `stk_gha`, `stk_gha_col`): **0 to 800** pax per 10 min.

Both ceilings are multiples of 100 and are set by the spikiest models (`EG5` / `ED5`,
peak density 0.1 per minute). Flatter models (e.g. `U1`) therefore sit low on these axes;
that is the intended cost of a shared scale.

## Conventions (carried from the model docs)

Each file keeps the project conventions: Computer Modern body with the Calibri title date,
title page, running footer (Moitra, Yash / page / June 2026), one figure per page, a legend
on every page (airline or GHA key for coloured views, capped to the top 20 airlines with a
"+N more" note; an element key for black views), HHMM time axis with correct base-60
arithmetic, and the mean entry time marked on per-flight curves.

## Notes

The curves are theoretical densities `f(t)` scaled to expected pax per 10-minute interval
(pax = round(LF x cap), LF = 1). Every model was checked to integrate to 1 over its support.
Render any file in RStudio (Knit) to get its PDF.
