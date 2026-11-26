#!/bin/bash
# usage: runmod.sh N -> mod_N.txt (n, vi, f), mod_dual_N.txt (n, atoms, coatoms, count)
N=$1; s=$(date +%s)
../src/modular_run $N mod_dual_$N.txt > mod_$N.txt 2> mod_$N.err & pid=$!
peak=0; while kill -0 $pid 2>/dev/null; do r=$(awk '/VmRSS/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$r" ] && [ "$r" -gt "$peak" ] && peak=$r; sleep 5; done
wait $pid; rc=$?
echo "mod_$N rc=$rc time=$(( $(date +%s) - s ))s peakRSS=${peak}KB" | tee -a runs.log
