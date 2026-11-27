#!/bin/bash
# usage: runmod2.sh N [THREADS] -> mod_N.txt, mod_dual_N.txt; resumes from ck_mod_N.bin if present
N=$1; T=${2:-4}; s=$(date +%s)
../src/layers2_mod $N mod_dual_$N.txt modular $T ck_mod_$N.bin > mod_$N.txt 2>> mod_$N.err & pid=$!
peak=0; while kill -0 $pid 2>/dev/null; do r=$(awk '/VmRSS/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$r" ] && [ "$r" -gt "$peak" ] && peak=$r; sleep 5; done
wait $pid; rc=$?
echo "mod_$N threads=$T rc=$rc time=$(( $(date +%s) - s ))s peakRSS=${peak}KB (since last (re)start)" | tee -a runs.log
