import os, sys, subprocess

sinklist =  ['']
def getSinks():
    sinkDetails = {}

    sinkDetails['alsa_output.pci-0000_03_00.1.3.pro-output-10'] = 'DP Headphone'
    sinkDetails['alsa_output.pci-0000_03_00.1.3.hdmi-stereo'] = 'HDMI Speaker'

    cmd = "pactl list sinks short  | awk '{print $2}'"
    sinks = subprocess.check_output(cmd, shell=True).decode('utf-8').split()
    for sink in sinks:
        name_cmd =  f"pactl list sinks | grep \"Name: {sink}\" -A 1 | tail -1 | tail -1 | sed  's|.*: ||'   "
        name = subprocess.check_output(name_cmd, shell=True).decode('utf-8')
        if "Loopback" in name or 'S/PDIF' in name or 'Radeon' in name or 'Navi' in name:
            continue
            print("\n\n\n\nyes\n\n\n\n")
            # sink
        sinkDetails[sink] = name.rstrip('\n')
        # sinkNames.append(name.rstrip('\n'))
    # return sinks, sinkNames


    return sinkDetails

print(getSinks())

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
    if  "Audio__" in key:
        return "idk"
    if  "hdmi" in key:
        return "hdmi"

def switch(sink,name):
    bashCommand = f"sh -c pulsevol -s {sink} {name}"
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