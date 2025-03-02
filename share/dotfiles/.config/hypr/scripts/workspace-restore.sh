#!/bin/bash

total_monitors=$(hyprctl monitors -j | jq length)
monitor_names=($(hyprctl monitors -j | jq '.[].name'))

# Loop through the names and perform actions
for name in "${monitor_names[@]}"; do
    echo "Name: $name"
    # You can add more actions here
done

if [[ $total_monitors == 2 ]];then
    echo "two monitors"
    left_monitor="$(hyprctl monitors -j | jq -r '.[] | select(.x == 0) | .name')"
    right_monitor="$(hyprctl monitors -j | jq -r '.[] | select(.x == 2560) | .name')"
    echo $left_monitor $right_monitor
    hyprctl dispatch moveworkspacetomonitor 1 "$left_monitor"
    hyprctl dispatch moveworkspacetomonitor 5 "$left_monitor"

    hyprctl dispatch moveworkspacetomonitor 2 "$right_monitor"
    hyprctl dispatch moveworkspacetomonitor 3 "$right_monitor"
    hyprctl dispatch moveworkspacetomonitor 4 "$right_monitor"
    notify-send "Shikane" "workspaces restored" -i hyprland

elif [[ $total_monitors == 1 ]];then
    echo "single monitors"
    monitor="$(hyprctl monitors -j | jq -r '.[] | select(.x == 0) | .name')"
    echo $monitor
    # hyprctl dispatch moveworkspacetomonitor 1 "$monitor"
    # hyprctl dispatch moveworkspacetomonitor 5 "$monitor"

    # hyprctl dispatch moveworkspacetomonitor 2 "$monitor"
    # hyprctl dispatch moveworkspacetomonitor 3 "$monitor"
    # hyprctl dispatch moveworkspacetomonitor 4 "$monitor"

fi


