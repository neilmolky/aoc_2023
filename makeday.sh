#!/bin/bash

day=$1

mkdir "day_$day"
cd "day_$day"
touch data.txt
touch test1.txt
touch test2.txt
touch part1.py
touch part2.py

echo "created folder: day_$day"
echo "with files"
ls