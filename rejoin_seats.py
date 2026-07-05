#!/usr/bin/env python3
"""Rejoin seats.xlsx from its split parts and verify the checksum.

The seat-level master seats.xlsx (19 MB) is carried in this repository as
exact binary parts, seats.xlsx.part-NN.bin, because of a transfer-size
limit in the publication pipeline. Running

    python3 rejoin_seats.py

concatenates the parts into seats.xlsx and verifies it against
seats.xlsx.sha256. Equivalent one-liners:
  Linux/macOS:  cat seats.xlsx.part-*.bin > seats.xlsx
  Windows:      copy /b seats.xlsx.part-00.bin+seats.xlsx.part-01.bin+... seats.xlsx

Author: Yash Moitra, Delhi International Airport Limited.
"""
import glob, hashlib, sys

parts = sorted(glob.glob("seats.xlsx.part-*.bin"))
if not parts:
    sys.exit("no parts found; run from the repository root")
h = hashlib.sha256()
with open("seats.xlsx", "wb") as out:
    for p in parts:
        with open(p, "rb") as fh:
            while chunk := fh.read(1 << 20):
                out.write(chunk); h.update(chunk)
want = open("seats.xlsx.sha256").read().split()[0]
got = h.hexdigest()
print("parts   :", ", ".join(parts))
print("sha256  :", got)
print("expected:", want)
sys.exit(0 if got == want else "CHECKSUM MISMATCH - do not use the file")
