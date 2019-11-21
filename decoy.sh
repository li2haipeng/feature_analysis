#!/usr/bin/env bash

for f in /home/lhp/PycharmProjects/feature_analysis/chunks/*csv
do
  python3 decoy.py "$f"
done
