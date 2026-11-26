#!/bin/bash
# Build the bounded-width automata for W = 2..WMAX, compute their growth rates and certify the
# lower bounds in exact arithmetic.  Writes data/bounded_growth.txt and data/bounded_certificates.txt.
# usage: scripts/run_bounded.sh [WMAX=12] [workdir]
set -e
cd "$(dirname "$0")/.."
WMAX=${1:-12}; DIR=${2:-$(mktemp -d)}
[ -x src/bounded ] || g++ -O2 -march=native -o src/bounded src/bounded.cpp -lnauty
: > data/bounded_growth.txt
for w in $(seq 2 $WMAX); do
  src/bounded $w $DIR/a$w.txt 2> $DIR/a$w.err
  st=$(sed -n 's/.*states=\([0-9]*\) transitions=\([0-9]*\).*/\1 \2/p' $DIR/a$w.err)
  g=$(python3 scripts/bounded_growth.py $DIR/a$w.txt 30 | sed -n 's/^growth rate.*: //p' | tr '\n' ' ')
  echo "$w $st $g" | tee -a data/bounded_growth.txt     # W states transitions growth(all) growth(v.i.)
done
{ python3 scripts/bounded_certificate.py $DIR/a6.txt vi 1.7262
  python3 scripts/bounded_certificate.py $DIR/a$WMAX.txt vi 1.7265363
  python3 scripts/bounded_certificate.py $DIR/a$WMAX.txt all 1.84337061; } | tee data/bounded_certificates.txt
