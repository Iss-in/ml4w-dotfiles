#!/bin/bash
source /home/kushy/Syncthing/Projects/Shoonya/venv/bin/activate
cd /home/kushy/.config/waybar/scripts/
# python $HOME/.config/waybar/scripts/shoonya_taskbar.py --getBarInfo
# exit 0  

getOtmOptions() {
    python $HOME/.config/waybar/scripts/shoonya_taskbar.py --getBarInfoOption
}

getPnl() {
    python $HOME/.config/waybar/scripts/shoonya_taskbar.py --getBarInfo
}
verbose='false'
while getopts 'opv' flag; do
  case "${flag}" in
    o)  getOtmOptions
	    ;;
    p)  getPnl
	    ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done

