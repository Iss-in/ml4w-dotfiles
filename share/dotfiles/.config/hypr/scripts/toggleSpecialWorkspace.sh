#!/bin/bash

# if speical workspace is active , toggle it, otherwise send it back to special workspace

workspace=$(hyprctl activewindow -j | jq '.workspace.name' | sed 's|.*:||;s|\"||')
is_special=$(hyprctl activewindow -j | jq '.workspace.name' | grep special)

if [ -z $is_special ];then
    hyprctl dispatch movetoworkspacesilent special
else
    hyprctl dispatch togglespecialworkspace $workspace
fi