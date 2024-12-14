#!/bin/bash
# current_workspace=$(hyprctl activeworkspace -j | jq '.id' )
# nautilus_address=$(hyprctl clients -j | jq -r '.[] | select(.class == "org.gnome.Nautilus") | .address')
# nautilus_workspace=$(hyprctl clients -j | jq -r '.[] | select(.class == "org.gnome.Nautilus") | .workspace.id')

# nautlus_scratchpad="special"
# sticky_scratchpad="sticky"

# if [ -z $nautilus_workspace ] ;then
#     echo "no nautilus window"
#     nautilus -w & disown
# elif [ $current_workspace -ne $nautilus_workspace ]; then
#     echo "nautilus in another workspace"
#     echo \"$current_workspace,address:$nautilus_address\"
#     hyprctl dispatch movetoworkspacesilent "$current_workspace,address:$nautilus_address"
# else
#     # echo "nautilus in same workspace"
#     hyprctl dispatch movetoworkspacesilent "name:$scratchpad,address:$nautilus_address"
# fi


current_workspace=$(hyprctl activeworkspace -j | jq '.id' )

toggle_app() {

    class="$1"
    run_command="$2"
    workspace="$3"

    echo $class $run_command $workspace
    app_workspace=$(hyprctl clients -j | jq --arg class $class -r '.[] | select(.class == $class) | .workspace.id')

    address=$(hyprctl clients -j | jq --arg class $class -r '.[] | select(.class == $class) | .address')

    if [ -z $app_workspace ] ;then
        echo "no window"
        # nautilus -w & disown
        eval "$run_command" & disown
        hyprctl dispatch togglespecialworkspace $workspace
    elif [ $current_workspace -ne $app_workspace ]; then
        echo "app in another workspace {app_workspace}"
        echo \"$current_workspace,address:$address\"
        hyprctl dispatch movetoworkspacesilent "$current_workspace,address:$address"
    else
        echo "nautilus in same workspace $app_workspace, moving to special:$workspace"
        hyprctl dispatch movetoworkspacesilent "special:${workspace},address:$address"
    fi
}


toggle_workspace() {

    class="$1"
    run_command="$2"
    workspace="$3"

    echo $class $run_command $workspace
    app_workspace=$(hyprctl clients -j | jq --arg class $class -r '.[] | select(.class == $class) | .workspace.id')

    address=$(hyprctl clients -j | jq --arg class $class -r '.[] | select(.class == $class) | .address')

    if [ -z $app_workspace ] ;then
        echo "no window"
        # nautilus -w & disown
        eval "$2" & disown
    fi
    hyprctl dispatch togglespecialworkspace $workspace
    # fi
}

#!/bin/bash
verbose='false'
while getopts 'nsv' flag; do
  case "${flag}" in
    n)  class="org.gnome.Nautilus" 
        run_command="nautilus -w"
        workspace="nautilus"
        toggle_workspace "$class" "$run_command" "$workspace"
	    ;;
    s)  class="com.vixalien.sticky" 
        run_command="sticky-notes"
        workspace="sticky"
        toggle_app "$class" "$run_command" "$workspace"
        # toggle_workspace "$class" "$run_command" "$workspace"
	    ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done

exec 101> "/tmp/toggle_floating.lock"
if ! flock -n 101; then
    printf 'another instance is running\n';
    exit 1
fi