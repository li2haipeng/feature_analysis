#!/usr/bin/env bash

#for i in 5 6 7 8
#do
#    for f in csv/gamma/"$i"/*.csv; do
#        python3 adapt_padding.py -pc "$f" -f "$i" -eps 0.005
#    done
#done
#
for i in 1 2 3 4
do
    for f in /home/lhp/PycharmProjects/dataset/Alexa_dataset/csv/"$i"/*.csv; do
        python3 laplace.py -pc "$f" -f "$i" -eps 0.05
    done
done