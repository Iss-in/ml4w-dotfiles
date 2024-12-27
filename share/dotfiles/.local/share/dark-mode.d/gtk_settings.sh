#!/bin/bash
GNOME_SCHEMA="org.gnome.desktop.interface"
ICON_DARK_THEME="Yaru-red-dark"
GTK_THEME="Yaru-red-dark"
GTK_THEME="Adwaita-dark"
COLOR_SCHEME="prefer-dark"

export PATH=/home/kushy/.local/bin/:/bin/:$PATH
COMIC_DIR='/home/kushy/tmp/strange_planet/nathanwpyle'

ln -sf /home/kushy/.config/sway/themes/vscode.json /home/kushy/.config/sway/themes/colorscheme.json
ln -sf /home/kushy/.config/hypr/conf/misc/dark.conf /home/kushy/.config/hypr/conf/misc/default.conf

# ln -sf /home/kushy/.icons/custom-dark/scalable/apps/joplin.png /home/kushy/.icons/default/joplin.png 
# ln -sf /home/kushy/.icons/custom/scalable/apps/albert-dark.svg /home/kushy/.icons/default/albert.svg
# ln -sf ~/.cache/wal/dunstrc_dark ~/.config/dunst/dunstrc
chmod +x /home/kushy/.config/sway/sway-colors


gsettings set "$GNOME_SCHEMA" gtk-theme "$GTK_THEME"

gsettings set "$GNOME_SCHEMA" color-scheme "$COLOR_SCHEME"
# /home/kushy/.config/sway/sway-colors
# killall dunst
# gammastep -O 3400

# wal -f /home/kushy/.config/sway/themes/colorscheme.json 

wal -q -i "$HOME/.config/ml4w/cache/current_wallpaper.png"

ln -sf /home/kushy/.cache/wal/sway-dark  /home/kushy/.config/sway/sway-colors
/home/kushy/.config/sway/sway-colors

sed -i 's|Light+|Dark+|' ~/.config/VSCodium/User/settings.json
# pkill hyprsunset
# pgrep hyprsunset || hyprsunset --temperature 4000 & disown
# sleep 1
hyprctl reload
# hyprshade on "blue-light-filter"
