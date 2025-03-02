#!/bin/bash

# Function to get the current volume levels of all sink inputs
get_volume_levels() {
    pactl list sink-inputs | grep -E 'Sink Input|Volume:' | awk 'NR % 2 {printf "%s ", $3} !(NR % 2) {print $5}'
}

# Function to set the volume level of a sink input
set_volume_level() {
    local input=$1
    input="${input:1}"
    local volume=$2
    pactl set-sink-input-volume "$input" "$volume"
}

# Function to lower the volume of all sink inputs by 50%
lower_volume() {
    local volume_levels=$(get_volume_levels)
    local volume_data=($volume_levels)
    
    for ((i = 0; i < ${#volume_data[@]}; i+=2)); do
        local input=${volume_data[i]}
        local volume=${volume_data[i+1]}

        # Remove the trailing '%' and calculate the new volume level (50% of the current volume)
        volume=${volume%\%}
        local new_volume=$((volume /  4 * 3 ))
        new_volume="${new_volume}%"

        # Store the original volume in an associative array
        original_volumes[$input]=$volume

        # Set the new volume level
        echo $input
        set_volume_level "$input" "$new_volume"
    done
}

# Function to restore the original volume levels
restore_volume() {
    for input in "${!original_volumes[@]}"; do
        set_volume_level "$input" "${original_volumes[$input]}%"
    done
}

# Function to play the notification sound
play_notification_sound() {
    lower_volume

    # Play the notification sound (replace with your actual notification sound file)
    paplay /home/kushy/.config/swaync/sounds/ping.wav

    # Wait for the notification sound to finish (optional sleep if needed)
    # sleep 2

    restore_volume
}

# Declare an associative array to store original volumes
declare -A original_volumes

# Call the function to play the notification sound
play_notification_sound