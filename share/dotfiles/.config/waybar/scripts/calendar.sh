#!/bin/bash

monitor=$(swaymsg -t get_outputs --raw | jq '. | map(select(.focused == true)) | .[0].name' -r)
if [[ $monitor == 'DP-1' ]]; then
    screen=1
else
    screen=0
fi
# echo $screen
eww open --toggle info-center --screen $screen
eww open --toggle info-center-closer --screen $screen