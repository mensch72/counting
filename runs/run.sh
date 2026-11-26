#!/bin/bash
# usage: run.sh N [atoms]  -> writes vi_N[_tA].txt, logs peak memory
N=$1; T=$2; tag="vi_$N"; [ -n "$T" ] && tag="dual_${N}_t$T"
s=$(date +%s)
../src/frontier2 $N $T > $tag.txt 2> $tag.err & pid=$!
peak=0; while kill -0 $pid 2>/dev/null; do r=$(awk '/VmRSS/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$r" ] && [ "$r" -gt "$peak" ] && peak=$r; sleep 2; done
wait $pid; rc=$?
echo "$tag rc=$rc time=$(( $(date +%s) - s ))s peakRSS=${peak}KB" | tee -a runs.log
