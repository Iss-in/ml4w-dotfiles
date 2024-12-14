#!/bin/bash

file="/tmp/trade_counter.json"

# notify-send hello kys

new_date=$(date '+%d/%m/%g')

getEvents(){
    day=$1
    new_date=$(date '+%d/%m/%Y' -d "+ $day days")
    khal list $new_date | tail -n +2 | sed 's|.*PM ||' | sed  's/^/ - /'
}

verbose='false'
while getopts 'g:pls:v' flag; do
  case "${flag}" in
    g) val=${OPTARG}
        getEvents $val;;
    p) getPnl;;
    l) getMaxLoss;;
    s)  val="${OPTARG}"
        set_volume $val
        #pactl -- set-sink-volume $sink $val%
        ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done


