# -*- coding: utf-8 -*-

"""
Takes arguments in the form of '`[[hrs:]mins:]secs [name]`'. Empty fields resolve to `0`. \
Fields exceeding the maximum amount of the time interval are automatically refactorized.

Examples:
- `5:` starts a 5 minutes timer
- `1:: ` starts a 1 hour timer
- `120:` starts a 2 hours timer
"""

import os,sys,dbus,subprocess
import threading
from datetime import timedelta
from pathlib import Path
from time import strftime, time, localtime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from query_parser import parse_query, ParseQueryError
from notifypy import Notify
from albert import *

from media import get_icon_path, play_sound



md_iid = '2.0'
md_version = "1.7"
md_name = "Timer2"
md_description = "Set up timers"
md_license = "BSD-2"
md_url = "https://github.com/albertlauncher/python/tree/master/timer"
md_maintainers = ["@manuelschneid3r", "@googol42", "@uztnus"]


class Timer(threading.Timer):

    def __init__(self, interval, name, callback):
        super().__init__(interval=interval,
                         function=lambda: callback(self))
        self.name = name
        self.begin = int(time())
        self.end = self.begin + interval
        self.start()
        print("new timer",self.name, self.begin, self.end, flush=True)


class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        TriggerQueryHandler.__init__(self,
                                     id=md_id,
                                     name=md_name,
                                     description=md_description,
                                     synopsis='[1h2m3s] [name]',
                                     defaultTrigger='timer ')
        PluginInstance.__init__(self, extensions=[self])
        self.iconUrls = [f"file:{Path(__file__).parent}/images/icon.png"]
        self.soundPath = Path(__file__).parent / "bing.wav"
        self.timers = []
        self.notification = None

    def finalize(self):
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()

    def SendNotification(self, title, body):
        notification = Notify()
        notification.title = title
        notification.message = body
        notification.icon = "/home/kushy/.local/share/albert/python/plugins/timer_new/images/icon.png"

        notification.send()
    def startTimer(self, interval, name):
        timer = Timer(interval, name, self.onTimerTimeout)
        self.timers.append(timer)

        title=f"{'Timer Started '}"
        body=f"Will Time out at {strftime('%X', localtime(timer.end))}"
        self.notification = self.SendNotification(title,body)
        
        # notify = dbus.Interface(dbus.SessionBus().get_object(bus_name, object_path), interface)
        # notify.Notify(md_name, 0, self.iconUrls, title, text, [], {"urgency":2}, 1000)


    def deleteTimer(self, timer):
        self.timers.remove(timer)
        timer.cancel()


    def onTimerTimeout(self, timer):
        title=f"{timer.name if timer.name else 'Time is up'}"
        print(f"timeout, {title}", flush=True)
        body=f"Timed out at {strftime('%X', localtime(timer.end))}"

        self.SendNotification(title,body)
        play_sound()
        # subprocess.run(["espeak-ng","Timer is finished","-s 160"], check=True, text=True)
        self.deleteTimer(timer)
        print(f"timer deleted")

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return

        if query.string.strip():
            try:
                time_sec, delta, message = parse_query(query.string)
            except:
                return StandardItem(
                    id=self.name,
                    text="Invalid input",
                    # subtext="Enter a query in the form of '%s[1h2m3s] [name]'" % self.defaultTrigger(),
                    subtext="Enter a query in the form of [1h2m3s]",
                    iconUrls=self.iconUrls,
                )
            seconds = time_sec
            name = message

            query.add(StandardItem(
                id=self.name,
                text=str(timedelta(seconds=seconds)),
                subtext='Set a timer with name "%s"' % name if name else 'Set a timer',
                iconUrls=self.iconUrls,
                actions=[Action("set-timer", "Set timer", lambda sec=seconds: self.startTimer(sec, name))]
            ))
            return

        # List timers
        items = []
        for timer in self.timers:
            m, s = divmod(timer.interval, 60)
            h, m = divmod(m, 60)
            identifier = "%d:%02d:%02d" % (h, m, s)

            timer_name_with_quotes = '"%s"' % timer.name if timer.name else ''
            items.append(StandardItem(
                id=self.name,
                text='Delete timer %s [%s]' % (timer_name_with_quotes, identifier),
                subtext="Times out %s" % strftime("%X", localtime(timer.end)),
                iconUrls=self.iconUrls,
                actions=[Action("delete-timer", "Delete timer", lambda t=timer: self.deleteTimer(t))]
            ))

        if items:
            query.add(items)