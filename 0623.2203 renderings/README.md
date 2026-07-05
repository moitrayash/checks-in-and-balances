# Per-model renderings

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** July 05, 2026

One family of exhibits per entry-time model (104 models, N1 to SR39), five views each,
plain and coloured. File pattern: `<MODEL>__<view>[_col].Rmd` and `.pdf`.

| View | Content |
|---|---|
| `curves` | The model's entry-time density per flight, one page per flight, over clock time |
| `comp` | Composite: all flights' densities overlaid on one axis |
| `stk_air` | Stacked view aggregated by airline |
| `stk_gha` | Stacked view aggregated by ground handler |
| `_col` variants | The same, coloured |

## Render status

`.Rmd` sources are present and complete for all 104 models and all views (832 files).
The PDF sweep was in progress at handoff: the stacked-GHA series is essentially complete
(101 plain, 100 coloured), the other views are partial (24 `stk_air`, 13 `stk_air_col`,
and a handful of `comp` and `curves` renders). Any missing or additional PDF can be
produced by knitting the corresponding `.Rmd` (R, knitr, XeLaTeX, Latin Modern fonts).

Eighteen PDFs were found byte-truncated (interrupted writes; unreadable in any viewer)
and are quarantined in `_corrupt (unreadable, re-knit from Rmd)/`; their sources are
intact, so re-knitting regenerates them.

All readable PDFs carry the project watermark and the corrected title page. The
whole-day, reference-model versions of these views also exist at the repository root
(`curves.pdf`, `compcurves*.pdf`), and the interactive equivalents are in
`dashboard/index.html` (Arrivals Lab).
