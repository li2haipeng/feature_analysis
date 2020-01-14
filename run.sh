#!/usr/bin/env bash

for folder in /home/lhp/PycharmProjects/dataset/Video_dataset/csv/*
do
  echo "$folder"
  for files in "$folder"/*
  do
    python3 data_preproc.py "$files" 0.5
  done
done

for folder in /home/lhp/PycharmProjects/dataset/Video_dataset/csv/*
do
  echo "$folder"
  for files in "$folder"/*
  do
    python3 data_preproc.py "$files" 1.0
  done
done

for folder in /home/lhp/PycharmProjects/dataset/Video_dataset/csv/*
do
  echo "$folder"
  for files in "$folder"/*
  do
    python3 data_preproc.py "$files" 2.0
  done
done

for folder in /home/lhp/PycharmProjects/dataset/Video_dataset/csv/*
do
  echo "$folder"
  for files in "$folder"/*
  do
    python3 data_preproc.py "$files" 0.05
  done
done
#for folder in /home/lhp/PycharmProjects/dataset/Alexa_dataset/sel_defense/dp/*
#do
#  echo "$folder"
#  python3 data_preproc.py "$folder"
#done