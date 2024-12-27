#!/usr/bin/env sh

# script for change workspaces in each monitor independently
# on the Hyprland Wayland compositor/ WM

monitor=$(hyprctl activeworkspace | grep -v grep |  grep 'monitorID') #get active monitor
space=$( hyprctl activeworkspace | grep 'workspace ' | grep -v grep |  awk {'print $3'}) #get active workspace
spaces=$(hyprctl workspaces | grep -B 2 "$monitor" | grep -v grep  | grep -v special | grep workspace | awk {'print $3'}) #get workspaces on the same monitor
position=$(echo "$spaces" | grep -v grep | grep -n $space | cut -d ":" -f 1) #learn in which position of the workspaces list this workspace is (i.e 1st, 2nd, etc.)


# dont do anything if monitor has single workspace, because it will then switch to previous active workspace on any monitor
if [[ $(echo "$spaces" | wc -l) -eq 1 ]];then
  exit 0
fi


echo $monitor 
echo $space 
echo $spaces 
echo $position
# choose next or previous workspace according to input
# if on the first or last workspace, cycle to the last or first

get_target () {
    case $1 in
    next) 
        if [[ "$position" == $(echo "$spaces" | wc -l) ]]; then
        target=1
        else
        target=$(($position + 1))
    fi;;
    prev)
        if [[ "$position" == 1 ]]; then
        target=$(echo "$spaces" | wc -l) 
        else
        target=$(($position - 1))
    fi;;
    *) 
        echo 'error: please specify "next" or "prev"'
        exit;;
    esac
}

get_target $1 
worksp_target=$(echo "$spaces" | sed "${target}q;d")

echo target $target
echo "worksp_target $worksp_target "

# the previous "case" loop selected a Nth workspace from the available list
# the below command will choose the ID of that Nth workspace 
# to generate the hyprland dispatcher accordingly


# dont do anything if target workspace has no window
windowcount=$(hyprctl clients | grep -v grep | grep "workspace: $worksp_target"  | wc -l)
while [[ windowcount -eq 0 ]]; do
    echo "workspace count for $worksp_target is 0"
    case $1 in
    next) 
        if [[ "$target" == $(echo "$spaces" | wc -l) ]]; then
            echo "target exceed last workspace, switching back to 1"
            target=1
        else
            target=$(($target + 1))
    fi;;
    prev)
        if [[ "$target" == 1 ]]; then
        target=$(echo "$spaces" | wc -l) 
        else
        target=$(($target - 1))
    fi;;
    *) 
        echo 'error: please specify "next" or "prev"'
        exit;;
    esac

    echo "new target is $target"
    worksp_target=$(echo "$spaces" | sed "${target}q;d")
    windowcount=$(hyprctl clients | grep -v grep | grep "workspace: $worksp_target"  | wc -l)
done

echo worksp_target $worksp_target


# skip if target is self
if [[ $space -eq $worksp_target ]];then
  exit 0
fi

hyprctl dispatch workspace $worksp_target
