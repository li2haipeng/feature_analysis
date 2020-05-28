#!/usr/bin/env bash

for method in 'mi'
do
  for b in '0.05'
  do
    for r in 60
    do
      for eps in 0.0005
      do
        python3 laplace_weight.py "$method" "$b" "$r" "$eps"
      done
    done
  done
done


#for b in '0.25'
#do
#  for r in 144
#  do
#    for eps in 0.05
#    do
#      python3 laplace_pfi.py "$b" "$r" "$eps"
#    done
#  done
#done

