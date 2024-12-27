import os,sys
# from albert import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(sys.path)
import audio_info
sinks = audio_info.getSinks()


for key in sinks:
    name = audio_info.getName(key)
    sink = key

    print(name,",",sink,flush=True)