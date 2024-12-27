"""
This extension provides a quick introduction on how to use the new Python pluging interface.
Hope you like it.
"""
import os,sys
from albert import *
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

# import audio_info
import audio_info2

md_iid = '2.0'
md_version = "1.3"
md_name = "Audio switcher "
md_description = "swith default audio device"
md_license = "BSD-3"
md_url = "https://github.com/albertlauncher/python/tree/master/kill"
md_maintainers = "@Pete-Hamlin"
md_credits = "Original idea by Benedict Dudel & Manuel Schneider"
iconUrls = [f"file:{Path(__file__).parent}/images/icon.svg"]
script_path = f"{Path(__file__).parent}/getTotp.sh"

class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        TriggerQueryHandler.__init__(self,
                                     id=md_id,
                                     name=md_name,
                                     description=md_description,
                                     defaultTrigger='aud ')
        PluginInstance.__init__(self, extensions=[self])
    

    def handleTriggerQuery(self, query):
        items = []
        q_string = query.string
        
        sinkDetails = audio_info2.getSinkDetails()
        
        print(f'sink details are {sinkDetails}' ,flush=True)
        for sink in sinkDetails:
            # name = audio_info.getName(yakey)
            name = sinkDetails[sink]
            # sink = key

            print(f'sink is {sink}, name is {name}',flush=True)

            # print(name,",",sink,flush=True)

            query.add(StandardItem(
                id="Id",
                text=name,
                subtext=sink,
                iconUrls=iconUrls,
                actions=[Action(name, sink, lambda n=name,s=sink: runDetachedProcess(["bash", "scripts/pulsevol2", "-s", s, n]))]
            ))

        query.add(items)