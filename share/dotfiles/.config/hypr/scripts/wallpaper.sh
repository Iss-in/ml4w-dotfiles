#!/bin/bash
#  _      __     ____                      
# | | /| / /__ _/ / /__  ___ ____  ___ ____
# | |/ |/ / _ `/ / / _ \/ _ `/ _ \/ -_) __/
# |__/|__/\_,_/_/_/ .__/\_,_/ .__/\__/_/   
#                /_/       /_/             
# -----------------------------------------------------
# Check to use wallpaper cache
# -----------------------------------------------------

use_cache=0
if [ -f ~/.config/ml4w/settings/wallpaper_cache ] ;then
    use_cache=1
fi

if [ "$use_cache" == "1" ] ;then
    echo ":: Using Wallpaper Cache"
else
    echo ":: Wallpaper Cache disabled"
fi

# -----------------------------------------------------
# Set defaults
# -----------------------------------------------------

force_generate=0
generated_versions="$HOME/.config/ml4w/cache/wallpaper-generated"
waypaper_running=$HOME/.config/ml4w/cache/waypaper-running
cache_file="$HOME/.config/ml4w/cache/current_wallpaper"
blurred_wallpaper="$HOME/.config/ml4w/cache/blurred_wallpaper.png"
square_wallpaper="$HOME/.config/ml4w/cache/square_wallpaper.png"
rasi_file="$HOME/.config/ml4w/cache/current_wallpaper.rasi"
blur_file="$HOME/.config/ml4w/settings/blur.sh"
default_wallpaper="$HOME/wallpaper/default.jpg"
current_wallpaper="$HOME/.config/ml4w/cache/current_wallpaper.png"

wallpaper_effect="$HOME/.config/ml4w/settings/wallpaper-effect.sh"
blur="50x30"
blur=$(cat $blur_file)


cp $1 $current_wallpaper

# Ensures that the script only run once if wallpaper effect enabled
if [ -f $waypaper_running ] ;then 
    rm $waypaper_running
    exit
fi

# Create folder with generated versions of wallpaper if not exists
if [ ! -d $generated_versions ] ;then
    mkdir $generated_versions
fi

# -----------------------------------------------------
# Get selected wallpaper
# -----------------------------------------------------

if [ -z $1 ] ;then
    if [ -f $cache_file ] ;then
        wallpaper=$(cat $cache_file)
    else
        wallpaper=$default_wallpaper
    fi
else
    wallpaper=$1
fi
used_wallpaper=$wallpaper
echo ":: Setting wallpaper with original image $wallpaper"
tmp_wallpaper=$wallpaper

# -----------------------------------------------------
# Copy path of current wallpaper to cache file
# -----------------------------------------------------

if [ ! -f $cache_file ] ;then
    touch $cache_file
fi
<<<<<<< HEAD
echo "$wallpaper" > $cache_file
echo ":: Path of current wallpaper copied to $cache_file"
=======
echo "$wallpaper" >$cachefile
echo ":: Path of current wallpaper copied to $cachefile"
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37

# -----------------------------------------------------
# Get wallpaper filename
<<<<<<< HEAD
# ----------------------------------------------------- 
wallpaper_filename=$(basename $wallpaper)
echo ":: Wallpaper Filename: $wallpaper_filename"
=======
# -----------------------------------------------------
wallpaperfilename=$(basename $wallpaper)
echo ":: Wallpaper Filename: $wallpaperfilename"
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37

# -----------------------------------------------------
# Wallpaper Effects
# -----------------------------------------------------

if [ -f $wallpaper_effect ] ;then
    effect=$(cat $wallpaper_effect)
    if [ ! "$effect" == "off" ] ;then
        used_wallpaper=$generated_versions/$effect-$wallpaper_filename
        if [ -f $generated_versions/$effect-$wallpaper_filename ] && [ "$force_generate" == "0" ] && [ "$use_cache" == "1" ] ;then
            echo ":: Use cached wallpaper $effect-$wallpaper_filename"
        else
<<<<<<< HEAD
            echo ":: Generate new cached wallpaper $effect-$wallpaper_filename with effect $effect"
            dunstify "Using wallpaper effect $effect..." "with image $wallpaper_filename" -h int:value:10 -h string:x-dunst-stack-tag:wallpaper
=======
            echo ":: Generate new cached wallpaper $effect-$wallpaperfilename with effect $effect"
            notify-send --replace-id=1 "Using wallpaper effect $effect..." "with image $wallpaperfilename" -h int:value:33
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37
            source $HOME/.config/hypr/effects/wallpaper/$effect
        fi
        echo ":: Loading wallpaper $generated_versions/$effect-$wallpaper_filename with effect $effect"
        echo ":: Setting wallpaper with $used_wallpaper"
        touch $waypaper_running
        waypaper --wallpaper $used_wallpaper
    else
        echo ":: Wallpaper effect is set to off"
    fi
else
    effect="off"
fi

<<<<<<< HEAD

# ----------------------------------------------------- 
=======
# -----------------------------------------------------
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37
# Execute pywal
# -----------------------------------------------------

echo ":: Execute pywal with $used_wallpaper"
if [[ $(darkman get) == "light" ]];then
    wal -q -l -i $used_wallpaper
else
    wal -q -i $used_wallpaper
fi
source "$HOME/.cache/wal/colors.sh"

# -----------------------------------------------------
# Walcord
# -----------------------------------------------------

if type walcord >/dev/null 2>&1; then
    walcord
fi

# -----------------------------------------------------
# Reload Waybar
# -----------------------------------------------------
<<<<<<< HEAD
~/.config/waybar/launch.sh

# ----------------------------------------------------- 
# Reload AGS
# -----------------------------------------------------
killall ags
ags &
eww reload
# ----------------------------------------------------- 
=======

killall -SIGUSR2 waybar

# -----------------------------------------------------
# Update Pywalfox
# -----------------------------------------------------

if type pywalfox >/dev/null 2>&1; then
    pywalfox update
fi

# -----------------------------------------------------
# Update SwayNC
# -----------------------------------------------------
sleep 0.1
swaync-client -rs

# -----------------------------------------------------
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37
# Created blurred wallpaper
# -----------------------------------------------------

if [ -f $generated_versions/blur-$blur-$effect-$wallpaper_filename.png ] && [ "$force_generate" == "0" ] && [ "$use_cache" == "1" ] ;then
    echo ":: Use cached wallpaper blur-$blur-$effect-$wallpaper_filename"
else
<<<<<<< HEAD
    echo ":: Generate new cached wallpaper blur-$blur-$effect-$wallpaper_filename with blur $blur"
    magick $used_wallpaper -resize 75% $blurred_wallpaper
=======
    echo ":: Generate new cached wallpaper blur-$blur-$effect-$wallpaperfilename with blur $blur"
    # notify-send --replace-id=1 "Generate new blurred version" "with blur $blur" -h int:value:66
    magick $used_wallpaper -resize 75% $blurredwallpaper
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37
    echo ":: Resized to 75%"
    if [ ! "$blur" == "0x0" ] ;then
        magick $blurred_wallpaper -blur $blur $blurred_wallpaper
        cp $blurred_wallpaper $generated_versions/blur-$blur-$effect-$wallpaper_filename.png
        echo ":: Blurred"
    fi
fi
cp $generated_versions/blur-$blur-$effect-$wallpaper_filename.png $blurred_wallpaper

# -----------------------------------------------------
# Create rasi file
# -----------------------------------------------------

if [ ! -f $rasi_file ] ;then
    touch $rasi_file
fi
<<<<<<< HEAD
echo "* { current-image: url(\"$blurred_wallpaper\", height); }" > "$rasi_file"
=======
echo "* { current-image: url(\"$blurredwallpaper\", height); }" >"$rasifile"
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37

# -----------------------------------------------------
# Created square wallpaper
# -----------------------------------------------------

<<<<<<< HEAD
echo ":: Generate new cached wallpaper square-$wallpaper_filename"
magick $tmp_wallpaper -gravity Center -extent 1:1 $square_wallpaper
cp $square_wallpaper $generated_versions/square-$wallpaper_filename.png
=======
echo ":: Generate new cached wallpaper square-$wallpaperfilename"
magick $tmpwallpaper -gravity Center -extent 1:1 $squarewallpaper
cp $squarewallpaper $generatedversions/square-$wallpaperfilename.png
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37
