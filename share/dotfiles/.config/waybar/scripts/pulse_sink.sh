# Get the default sink name
DEFAULT_SINK=$(pactl info | grep "Default Sink" | awk -F ': ' '{print $2}')

# Map sink names to icons
case "$DEFAULT_SINK" in
  *KM-HIFI*)
    ICON=""  # HDMI Icon
    ;;
  *pci*)
    ICON=""  # Headphones or Analog Speakers
    ;;
  *)
    ICON="󰖂"  # Default Speaker Icon
    ;;
esac

MUTED=$(pactl list sinks | grep -A 15 "$DEFAULT_SINK" | grep "Mute:" | awk '{print $2}')
# echo $MUTED
if [ "$MUTED" == "yes" ]; then
  ICON="  "
fi

# Output JSON for Waybar
echo "{\"text\": \"$ICON\", \"tooltip\": \"$DEFAULT_SINK\"}"
# kill -SIGRTMIN+9 waybar