import subprocess
from os.path import dirname, join

ICON_FILE = 'images/timer.png'
SOUND_FILE = "/usr/share/sounds/freedesktop/stereo/complete.oga"
_cached_icon_path = None


def get_icon_path():
    global _cached_icon_path
    if _cached_icon_path is None:
        _cached_icon_path = join(dirname(dirname(__file__)), ICON_FILE)
    return _cached_icon_path


def play_sound():
    subprocess.call(("cvlc" ,"--aout","pipewire-pulse", "--play-and-exit", SOUND_FILE))
play_sound()