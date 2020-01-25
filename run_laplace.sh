#!/usr/bin/env bash

for method in 'mi' 'jmim'
do
  for b in '0.25' '2.0'
  do
    for r in {2..10..2}
    do
      for eps in 0.000005 0.00005 0.0005 0.005
      do
        python3 laplace.py "$method" "$b" "$r" "$eps"
      done
    done
  done
done
