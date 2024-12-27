import os, sys, subprocess

sinklist =  ['']
def getSinkDetails():
    sinkDetails = {}

    cmd = "pactl list sinks short  | awk '{print $2}'"
    sinks = subprocess.check_output(cmd, shell=True).decode('utf-8').split()
    for sink in sinks:
        name = getName(sink)
        if name is not None:
            sinkDetails[sink] = name.rstrip('\n')
  
    return sinkDetails

def getSinks():
    sinks = {}

    cmd = "pactl list sinks short  | awk '{print $2}'"
    sinks = subprocess.check_output(cmd, shell=True).decode('utf-8').split()
  
    return sinks


def getDefaultSink():
    cmd = "pactl get-default-sink"
    sink = subprocess.check_output(cmd, shell=True).decode('utf-8').split()
    return sink

def getName(key):
    if "30_C0_1B_43_78_C5" in key:
        return "JBL Go+"
    if "74_45_CE_00_8B_1E" in key:
        return "WHCH512"
    if "0000_01_00" in key:
        return "System Speakers"
    if "0000_03_00" in key:
        return "Soundcore Motion"
    if "0000_05_00" in key:
        return "System Speakers"
    if "7C_96_D2_AD_3C_A8" in key:
        return "SoundCore Motion+"
    if "20_74_CF_A7_B1_E1" in key:
        return "Openmove"
    if  "KM-HIFI" in key:
        return "USB-C headphone"
    if  "Audio_3" in key:
        return "usb audio front"
    if  "Audio_1" in key:
        return "usb audio back"
    if  "analog-stereo" in key:
        return "Headphone aux"
    if  "hdmi" in key:
        return "Hdmi Speaker"


# print(getSinks())


def switch(sink,name):
    bashCommand = f"sh -c pulsevol2 -s {sink} \"{name}\""
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

# import sys
# # from albert import *
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(sys.path)
# print(switch(1,2))

# sinks = getSinks()
# for key in sinks:
#     name = getName(key)
#     sink = key

#     print(name,",",sink,flush=True)