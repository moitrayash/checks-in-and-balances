#!/usr/bin/env bash
# Render all model documents to Computer Modern PDFs (XeLaTeX) with the title page,
# Author: Yash Moitra, Delhi International Airport Limited.
# Contents page, and running footer defined in template.tex.
# Date is set in Calibri (Carlito); body is Latin Modern (Computer Modern).
set -e
cd "$(dirname "$0")"
mkdir -p docs
TITLEDATE="June 19, 2026"
FOOTERDATE="June 2026"
# Normalize non-ASCII math symbols so the LaTeX run is robust.
SAN='s/\x{2264}/<=/g; s/\x{2265}/>=/g; s/\x{2208}/ in /g; s/\x{2286}/ subset of /g; s/\x{00D7}/x/g; s/\x{00B7}/./g; s/\x{2211}/sum /g; s/\x{03A3}/sum /g; s/\x{2192}/ to /g; s/\x{2248}/~/g; s/\x{03C4}/tau/g; s/\x{03BC}/mu/g; s/\x{2014}/-/g; s/\x{2013}/-/g; s/\x{2212}/-/g;'
emit () {  # $1 = file base, $2 = document name on title page
  sed -e '/^# /d' -e '/^\*\*Author:\*\*/d' -e '/^\*\*Institution:\*\*/d' -e '/^\*\*Date:\*\*/d' "$1.md" \
    | perl -CSD -pe "$SAN" | iconv -c -f utf-8 -t ascii > "/tmp/$1.body.md"
  pandoc "/tmp/$1.body.md" --template=template.tex --pdf-engine=xelatex --shift-heading-level-by=-1 \
    -V titledate="$TITLEDATE" -V footerdate="$FOOTERDATE" -V docname="$2" -o "docs/$1.pdf"
  echo "  built docs/$1.pdf"
}
emit 00_Ground_Rules "Ground Rules"
emit Variable_Names  "Variable Names"
emit Definitions     "Definitions"
emit Methodology     "Methodology"
emit Model_Overview  "Overview"
TITLEDATE="July 05, 2026"; FOOTERDATE="July 2026"
emit README          "Read Me"
emit DATA_DICTIONARY "Data Dictionary"
emit INSIGHTS        "Insights"
