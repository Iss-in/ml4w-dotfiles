#!/bin/bash

dir="/home.kushy"
dir="$( dirname $0)"
source $dir/trade/bin/activate

getTrades() {
  python $dir/trade_counter.py --getTradeCount
}

getMaxLoss(){
  python $dir/trade_counter.py --getMaxLoss
}

getPnl() {
  python $dir/trade_counter.py --getPnl
}

getLatestCE() {
    python $dir/trade_counter.py --getLatestCE
}

getLatestPE() {
    python $dir/trade_counter.py --getLatestPE
}

refresh() {
  trade_count=$(python $dir/trade_counter.py --getTradeCount)
  
}

verbose='false'
while getopts 'tplceus:v' flag; do
  case "${flag}" in
    r) refresh;;
    t) getTrades;;
    p) getPnl;;
    l) getMaxLoss;;
    c) checkvalidDay;;
    e) getLatestCE;;
    u) getLatestPE;;
    s)  val="${OPTARG}"
        set_volume $val
        #pactl -- set-sink-volume $sink $val%
        ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done


