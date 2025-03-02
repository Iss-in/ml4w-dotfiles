#!/bin/bash
set +e

date >> /tmp/test
# sleep 30


if [[ -z $(gsettings get org.gnome.desktop.interface gtk-theme | grep -i dark) ]]; then
    echo already light
    exit 0
fi





GNOME_SCHEMA="org.gnome.desktop.interface"
ICON_DARK_THEME="Yaru-red"
GTK_THEME="Yaru-red"
GTK_THEME="Adwaita"

COLOR_SCHEME="prefer-light"


gsettings set "$GNOME_SCHEMA" gtk-theme "$GTK_THEME"
gsettings set "$GNOME_SCHEMA" color-scheme "$COLOR_SCHEME"


if [[ $XDG_CURRENT_DESKTOP == "Hyprland" ]]; then
    ln -sf /home/kushy/.config/hypr/conf/misc/light.conf /home/kushy/.config/hypr/conf/misc/default.conf
    # hyprctl reload
elif [[ $XDG_CURRENT_DESKTOP == "sway" ]]; then
    ln -sf ~/.cache/wal/sway-light  /home/kushy/.config/sway/sway-colors
    bash /home/kushy/.config/sway/sway-colors
fi

wal -q -l -i "$HOME/.config/ml4w/cache/current_wallpaper.png"
sed -i 's|Dark+|Light+|' ~/.config/VSCodium/User/settings.json


sed -i "s/color_scheme_path=.*/color_scheme_path=\"\/usr\/share\/color-schemes\/BreezeLight.colors\"/" /home/kushy/.config/qt6ct/qt6ct.conf

# darkman set light
