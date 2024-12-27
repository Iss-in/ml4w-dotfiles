"""Get TOTP for shoonya login"""

import os
import pyotp
from pathlib import Path

from signal import SIGKILL, SIGTERM

from albert import *

md_iid = '2.0'
md_version = "1.3"
md_name = "Shoonya TOTP"
md_description = "get Shoonya totp"
md_lib_dependencies = "pyotp"
md_license = "BSD-3"
md_url = "https://github.com/albertlauncher/python/tree/master/kill"
md_maintainers = "@Pete-Hamlin"
md_credits = "Original idea by Benedict Dudel & Manuel Schneider"
iconUrls = [f"file:{Path(__file__).parent}/images/icon.png"]
script_path = f"{Path(__file__).parent}/getTotp.sh"
class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        TriggerQueryHandler.__init__(self,
                                     id=md_id,
                                     name=md_name,
                                     description=md_description,
                                     defaultTrigger='otp ')
        PluginInstance.__init__(self, extensions=[self])

    def handleTriggerQuery(self, query):

        # totp = pyotp.TOTP('H32LR7H4W3O7A53XN53BSV554JRC5RIA').now()
        totp = '1234'
        results = []
        rank_items = []
        query.add(StandardItem(
                id="1",
                iconUrls=iconUrls,
                text='generate shoonya totp',
                subtext='press enter to copy totp to clipboard',
                actions=[
                    Action(
                        "totp",
                        "copy to clipboard",
                        lambda script_path=script_path: runDetachedProcess(["bash", script_path, "-s"]) 
                    )
                ]
        ))
        
        query.add(StandardItem(
                id="2",
                iconUrls=iconUrls,
                text='generate zerodha totp',
                subtext='press enter to copy totp to clipboard',
                actions=[
                    Action(
                        "totp",
                        "copy to clipboard",
                        lambda script_path=script_path: runDetachedProcess(["bash", script_path, "-z"]) 
                    )
                ]
        ))
        

        query.add(StandardItem(
                id="3",
                iconUrls=iconUrls,
                text='generate upstox totp',
                subtext='press enter to copy totp to clipboard',
                actions=[
                    Action(
                        "totp",
                        "copy to clipboard",
                        lambda script_path=script_path: runDetachedProcess(["bash", script_path, "-u"]) 
                    )
                ]
        ))
        

        query.add(StandardItem(
                id="3",
                iconUrls=iconUrls,
                text='generate aws totp',
                subtext='press enter to copy totp to clipboard',
                actions=[
                    Action(
                        "totp",
                        "copy to clipboard",
                        lambda script_path=script_path: runDetachedProcess(["bash", script_path, "-a"]) 
                    )
                ]
        ))