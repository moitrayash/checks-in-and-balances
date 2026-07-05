# df1_load.R
# Loads the T3 international-departures schedule OCR'd from df1.pdf.
# 161 flights | date 2026-06-21 | IGI Airport (DEL), Terminal 3.
#
# Column mapping (clean name  <-  original PDF header):
#   date               <- DATE                (all 2026-06-21)
#   airline_code       <- Airline code
#   flight_designator  <- Flight Designator
#   sobt               <- SOBT                (scheduled off-block time, HH:MM)
#   hour               <- Hour                (integer hour of SOBT, 0-23)
#   routing            <- Routing
#   traffic_type       <- Traffic Type        (all INTERNATIONAL)
#   public_terminal    <- Public Terminal     (all Terminal 3)
#   gha                <- GHA                  (ground handler: AISATS/BFS/IndiGo/Ramp 360)
#   seats              <- Seats
#   pax                <- Pax                  (= round(0.80 * seats))
#   d4_pax/d3_pax/d2_pax <- D-4 Pax/D-3 Pax/D-2 Pax (= round(0.30/0.40/0.30 * pax))
#   d4/d3/d2           <- D-4/D-3/D-2          (= SOBT minus 4/3/2 hours, HH:MM)
#
# NOTE: d4/d3/d2 are clock times. For early departures they roll past midnight
#       into the previous calendar day (e.g. SOBT 00:05 -> d4 20:05 on 2026-06-20).

# ---- tidyverse loader (recommended) ----
suppressWarnings(suppressMessages({
  library(readr)
  library(dplyr)
}))

df1 <- read_csv(
  "df1.csv",
  col_types = cols(
    date              = col_date("%Y-%m-%d"),
    airline_code      = col_character(),
    flight_designator = col_character(),
    sobt              = col_time("%H:%M"),
    hour              = col_integer(),
    routing           = col_character(),
    traffic_type      = col_factor(),
    public_terminal   = col_factor(),
    gha               = col_factor(),
    seats             = col_integer(),
    pax               = col_integer(),
    d4_pax            = col_integer(),
    d3_pax            = col_integer(),
    d2_pax            = col_integer(),
    d4                = col_time("%H:%M"),
    d3                = col_time("%H:%M"),
    d2                = col_time("%H:%M")
  )
)

str(df1)
# Quick checks
stopifnot(nrow(df1) == 161L)
# Example summaries:
# dplyr::count(df1, gha, sort = TRUE)
# aggregate(pax ~ hour, df1, sum)

# ---- base-R fallback (no packages) ----
# df1 <- read.csv("df1.csv", stringsAsFactors = FALSE)
# df1$date <- as.Date(df1$date)
# for (col in c("sobt","d4","d3","d2"))
#   df1[[col]] <- strptime(df1[[col]], "%H:%M")  # date part = today; use time only
