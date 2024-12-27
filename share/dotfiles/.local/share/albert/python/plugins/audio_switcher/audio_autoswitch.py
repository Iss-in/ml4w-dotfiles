import os,sys,subprocess
from pathlib import Path
import re 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# import audio_info
import audio_info2

import os
def switch(sink,name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    bashCommand = f"{dir_path}/scripts/pulsevol2 -s {sink} \"{name}\""
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


    bashCommand = f"pkill -SIGRTMIN+6 waybar"
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

default_sink = audio_info2.getDefaultSink()[0]
print(f'default sink is {default_sink}')
sinks = audio_info2.getSinks()
sinkDetails = audio_info2.getSinkDetails()
print(sinks)

# remove virtual/loopback sinks 
pattern = re.compile(r"virtual|loop",  re.IGNORECASE)
# Remove elements matching the pattern
sinks = [item for item in sinks if not pattern.search(item)]


default_sink_index = sinks.index(default_sink)
next_sink_index = ( default_sink_index + 1 ) % len(sinks)
next_sink = sinks[next_sink_index]
next_sink_name = sinkDetails[next_sink]
print(f'next sink is {next_sink_name} {next_sink}')
switch(next_sink,next_sink_name)