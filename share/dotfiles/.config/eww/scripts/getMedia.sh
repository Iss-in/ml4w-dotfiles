#!/bin/bash
#!/bin/bash



status=$(playerctl status)
title=$(playerctl metadata title)
artist=$(playerctl metadata artist)

image=$(/usr/bin/playerctl metadata  | grep artUrl | sed 's|^.*file://||')
ln -sf $image /tmp/music_widget.png


get_status() {
    if [[  $(/usr/bin/playerctl status) == "Playing" ]];then
        return 1
    fi
    return 0
}

get_symbol() {
    echo "♪"
}

get_title() {
    # title=${title:0:20}
    title=$(echo $title | sed 's/|.*//g;s/(.*//g')
    echo $title
}


get_artist() {
    artist=${artist:0:20}
    artist=$(echo $artist | sed 's/|.*//g;s/(.*//g')
    echo $artist
}



verbose='false'
while getopts 'stads:v' flag; do
  case "${flag}" in
    s)  val="${OPTARG}" 
        get_symbol
	    ;;
    t)  val="${OPTARG}" 
        get_title
	    ;;
    a)  val="${OPTARG}" 
        get_artist
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

# exec 26> "/tmp/get_media.lock"
# if ! flock -n 26; then
#     printf 'another instance is running\n';
#     exit 1
# fi