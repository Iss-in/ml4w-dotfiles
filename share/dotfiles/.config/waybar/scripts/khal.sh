#!/bin/bash

### usage
#### add weekly event to khal
#   khal new -a private 06/04/2023 08:00 AM  Weekly Expiry  -r weekly



status(){
    khal at  --format "{title}" | sed 1d | sed -z "s|\n|, |g;s|,.$||g"
}






verbose='false'
while getopts 'twa:d:sv' flag; do
  case "${flag}" in
    s)  status
	    ;;
    w)  val="${OPTARG}" 
        switch_source
	    ;;
    a)  val="${OPTARG}" 
        inc_volume $val
        #pactl -- set-sink-volume $sink +$val%
	    ;;
    d)  val="${OPTARG}" 
        pulseaudio-ctl down $val  &&     dunstify "Volume $volume" -h int:value:$(pamixer --get-volume) -a sound -r $msgId -u low
        ;;
    s)  val="${OPTARG}"
        set_volume $val
        #pactl -- set-sink-volume $sink $val%
        ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done

exec 27> "/tmp/khal.lock"
if ! flock -n 27  ; then
    printf 'another instance is running\n';
    exit 1
 fi