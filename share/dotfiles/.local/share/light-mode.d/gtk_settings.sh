#!/bin/bash
set +e
GNOME_SCHEMA="org.gnome.desktop.interface"
ICON_DARK_THEME="Yaru-red"
GTK_THEME="Yaru-red"
GTK_THEME="Adwaita"

COLOR_SCHEME="prefer-light"
export PATH=/home/kushy/.local/bin/:/bin/:$PATH

ln -sf /home/kushy/.config/sway/themes/light.json /home/kushy/.config/sway/themes/colorscheme.json
# ln -sf /home/kushy/.icons/custom/scalable/apps/joplin.png /home/kushy/.icons/default/joplin.png 
# ln -sf /home/kushy/.icons/custom/scalable/apps/albert-light.svg /home/kushy/.icons/default/albert.svg
# ln -sf ~/.cache/wal/dunstrc_light ~/.config/dunst/dunstrc
ln -sf /home/kushy/.config/hypr/conf/misc/light.conf /home/kushy/.config/hypr/conf/misc/default.conf


gsettings set "$GNOME_SCHEMA" gtk-theme "$GTK_THEME"
gsettings set "$GNOME_SCHEMA" color-scheme "$COLOR_SCHEME"
# echo $PATH 
# wal -f /home/kushy/.config/sway/themes/colorscheme.json 
sed -i 's|Dark+|Light+|' ~/.config/VSCodium/User/settings.json
ln -sf ~/.cache/wal/sway-light  /home/kushy/.config/sway/sway-colors
bash /home/kushy/.config/sway/sway-colors
# wal -f /home/kushy/.config/sway/themes/colorscheme.json 
wal -q -l -i "$HOME/.config/ml4w/cache/current_wallpaper.png"

# pkill hyprsunset
# pgrep hyprsunset || hyprsunset --temperature 6500 & disown
# hyprshade off
sleep 1
hyprctl reload

exit 0
# killall dunst
