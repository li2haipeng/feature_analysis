#!/usr/bin/env bash


for method in 'mrmr' 'jmim'
do
  for b in '0.05' '0.25' '0.5' '1.0' '2.0'
  do
    for r in {1..10..2}
    do
#      echo "$b" "$r" "$method"
      python3 jaccard.py "$b" "$r" "$method"
    done
  done
done