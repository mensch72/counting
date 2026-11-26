#!/bin/bash
# usage: runlay.sh MODE N -> lay_MODE_N.txt (n, vi, f), logs time and peak memory
M=$1; N=$2; s=$(date +%s)
../src/layers_geo $N - $M > lay_${M}_$N.txt 2> lay_${M}_$N.err & pid=$!
peak=0; while kill -0 $pid 2>/dev/null; do r=$(awk '/VmRSS/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$r" ] && [ "$r" -gt "$peak" ] && peak=$r; sleep 5; done
wait $pid; rc=$?
echo "lay_${M}_$N rc=$rc time=$(( $(date +%s) - s ))s peakRSS=${peak}KB" | tee -a runs.log
