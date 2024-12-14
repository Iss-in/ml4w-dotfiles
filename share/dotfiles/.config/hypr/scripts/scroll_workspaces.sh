#!/bin/bash

current_workspace=$(hyprctl activeworkspace -j | jq '.id' )
current_monitor=$(hyprctl activeworkspace -j | jq '.monitor' )
# current_monitorID=$(echo $current_monitorID | bc )

last_workspace=$(hyprctl workspaces -j  | jq --argjson monitor "$current_monitor" 'map(select(.monitor == $monitor and (.name | test("special") | not))) | max_by(.id) | .id')
first_workspace=$(hyprctl workspaces -j  | jq --argjson monitor "$current_monitor" 'map(select(.monitor == $monitor and (.name | test("special") | not))) | min_by(.id) | .id')




echo $current_workspace $current_monitor $last_workspace
if [ $current_workspace -lt $last_workspace ];then
    hyprctl dispatch workspace r+1
else
    hyprctl dispatch workspace $first_workspace
fi


