#!/bin/bash
min=$(date +%M)
min=$(echo $min | sed 's/^0*//')
min=$(( $min % 3 ))
min=$(( 2 - min ))


sec=$(date +%S)
sec=$(( 58 - sec ))
sec=$(printf "%02d\n" $sec)
echo $min:$sec
