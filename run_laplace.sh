#!/usr/bin/env bash

for method in 'mrmr' 'jmim'
do
  for b in '0.05' '0.25' '0.5' '1.0'
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

for b in '0.05' '0.25' '0.5' '1.0'
  do
    for r in {20..100..20}
    do
      for eps in 0.000005 0.00005 0.0005 0.005 0.05
      do
        python3 laplace.py mi "$b" "$r" "$eps"
      done
    done
done