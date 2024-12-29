#!/bin/bash
GNOME_SCHEMA="org.gnome.desktop.interface"
ICON_DARK_THEME="Yaru-red-dark"
GTK_THEME="Yaru-red-dark"
GTK_THEME="Adwaita-dark"
COLOR_SCHEME="prefer-dark"


gsettings set "$GNOME_SCHEMA" gtk-theme "$GTK_THEME"
gsettings set "$GNOME_SCHEMA" color-scheme "$COLOR_SCHEME"


if [[ $XDG_CURRENT_DESKTOP == "Hyprland" ]]; then
    ln -sf /home/kushy/.config/hypr/conf/misc/dark.conf /home/kushy/.config/hypr/conf/misc/default.conf
    hyprctl reload
elif [[ $XDG_CURRENT_DESKTOP == "sway" ]]; then
    ln -sf ~/.cache/wal/sway-dark  /home/kushy/.config/sway/sway-colors
    bash /home/kushy/.config/sway/sway-colors
fi

wal -q -l -i "$HOME/.config/ml4w/cache/current_wallpaper.png"



