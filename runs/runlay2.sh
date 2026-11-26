#!/bin/bash
# usage: runlay2.sh MODE N THREADS -> lay2_MODE_N.txt (n, vi, f); resumes from ck_MODE_N.bin if present
M=$1; N=$2; T=${3:-4}; s=$(date +%s)
../src/layers2_run $N - $M $T ck_${M}_$N.bin > lay2_${M}_$N.txt 2>> lay2_${M}_$N.err & pid=$!
peak=0; while kill -0 $pid 2>/dev/null; do r=$(awk '/VmRSS/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$r" ] && [ "$r" -gt "$peak" ] && peak=$r; sleep 5; done
wait $pid; rc=$?
echo "lay2_${M}_$N threads=$T rc=$rc time=$(( $(date +%s) - s ))s peakRSS=${peak}KB (time since last (re)start)" | tee -a runs.log
