#!/bin/bash
for i in {02..25}
do
    cp src/template.rs src/day$i.rs
    touch data/day$i.txt
done