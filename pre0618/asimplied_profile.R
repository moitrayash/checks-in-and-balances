# =====================================================================
#  asimplied_profile.R
#  Full descriptive profile of asimplied.csv
#  DEL departures schedule, 21-06-2026  (165 flights, 16 columns)
#
#  HOW TO RUN IN RSTUDIO:
#    Open this file, then click "Source" (or press Ctrl+Shift+S).
#    All output is wrapped in print()/cat() so it appears in the
#    Console even when the script is sourced.
# =====================================================================

path <- "C:/Users/yashm/OneDrive - Cornell University/Desktop/Work/Delhi International Airport Limited/Pax_Forecast_Model/asimplied.csv"

df <- read.csv(path, stringsAsFactors = TRUE, check.names = FALSE)

cat("\n=================== DIMENSIONS ===================\n")
cat("Rows   :", nrow(df), "\n")
cat("Columns:", ncol(df), "\n")

cat("\n=================== STRUCTURE: str() ===================\n")
str(df)

cat("\n=================== SUMMARY: every column ===================\n")
print(summary(df))

cat("\n=================== DISTINCT VALUES PER COLUMN ===================\n")
print(sapply(df, function(x) length(unique(x))))

cat("\n=================== NUMERIC PROFILE: Seats ===================\n")
cat("Non-missing :", sum(!is.na(df$Seats)), "of", nrow(df), "(",
    sum(is.na(df$Seats)), "missing )\n")
cat("Mean        :", round(mean(df$Seats, na.rm = TRUE), 1), "\n")
cat("Median      :", median(df$Seats, na.rm = TRUE), "\n")
cat("Std. Dev.   :", round(sd(df$Seats, na.rm = TRUE), 1), "\n")
cat("Min / Max   :", min(df$Seats, na.rm = TRUE), "/", max(df$Seats, na.rm = TRUE), "\n")
cat("Total seats :", sum(df$Seats, na.rm = TRUE), "\n")
cat("Quantiles   :\n"); print(quantile(df$Seats, na.rm = TRUE))

cat("\n=================== CATEGORICAL FREQUENCIES ===================\n")
cat_cols <- c("Airline code", "Traffic Type", "Public Terminal", "GHA",
              "Routing", "dest_iata", "dest_city", "dest_country",
              "airline_name", "airline_country")
for (col in cat_cols) {
  tb <- sort(table(df[[col]]), decreasing = TRUE)
  cat("\n---- ", col, "  (", length(tb), " distinct values ) ----\n", sep = "")
  if (length(tb) > 15) print(head(tb, 15)) else print(tb)
}

cat("\n=================== END OF PROFILE ===================\n")
