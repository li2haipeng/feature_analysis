#!/usr/bin/env bash



for b in '0.05' '0.25' '0.5' '1.0' '2.0'
do
#      echo "$b" "$r" "$method"
    python3 plus_analysis.py "$b"

done
