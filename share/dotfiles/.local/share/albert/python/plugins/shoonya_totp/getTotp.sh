#!/bin/bash
verbose='false'
while getopts 'szuva' flag; do
  case "${flag}" in
    s)  curl rpi:8000/getShoonyaTotp | sed s'|\"||g' | wl-copy 	    ;;
    z)  curl rpi:8000/getZerodhaTotp | sed s'|\"||g' | wl-copy	    ;;
    u)  curl rpi:8000/getUpstoxTotp | sed s'|\"||g' | wl-copy	    ;;
    a)  curl rpi:8000/getAwsTotp | sed s'|\"||g' | wl-copy	    ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done
