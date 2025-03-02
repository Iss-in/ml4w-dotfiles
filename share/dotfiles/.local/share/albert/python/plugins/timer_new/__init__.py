# -*- coding: utf-8 -*-

"""
Takes arguments in the form of '`[[hrs:]mins:]secs [name]`'. Empty fields resolve to `0`. \
Fields exceeding the maximum amount of the time interval are automatically refactorized.

Examples:
- `5:` starts a 5 minutes timer
- `1:: ` starts a 1 hour timer
- `120:` starts a 2 hours timer
"""

import os, sys, threading
from datetime import datetime, timedelta
from pathlib import Path
from time import strftime, time, localtime

from notifypy import Notify
from albert import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from media import get_icon_path, play_sound
from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop
from gi.repository import GLib
from query_parser import parse_query, ParseQueryError

md_iid = '2.0'
md_version = "1.7"
md_name = "Timer2"
md_description = "Set up timers"
md_lib_dependencies = ["dbus-python", "notify-py", "dasbus"]

md_license = "BSD-2"
md_url = "https://github.com/albertlauncher/python/tree/master/timer"
md_maintainers = ["@manuelschneid3r", "@googol42", "@uztnus"]

class Timer(threading.Timer):
    def __init__(self, interval, name, callback):
        super().__init__(interval=interval, function=lambda: callback(self))
        self.name = name
        self.begin = int(time())
        self.end = self.begin + interval
        self.start()
        self.notification_id = 0
        self.count = 0

        #print("new timer", self.name, self.begin, self.end, flush=True)

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

        self.loop = EventLoop()
        self.bus = SessionMessageBus()
        self.proxy = self.bus.get_proxy(
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications"
        )

        # Connect the NotificationClosed signal to the callback
        self.proxy.NotificationClosed.connect(self.on_notification_closed)

        # Start the event loop in a separate thread
        threading.Thread(target=self.loop.run, daemon=True).start()

    def finalize(self):
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()

    def SendNotification(self, title, body, timer, urgency='normal', ignore=False):
        notification = Notify()
        notification.title = title
        notification.message = body
        notification.application_name = "Albert"
        notification.urgency = 'critical'
        notification.icon = "/home/kushy/.local/share/albert/python/plugins/timer_new/images/icon.png"
        notification.actions = ["default", "OK"]

        # notification_id = notification.send()
        
        hints = {
            "urgency": GLib.Variant('y', 0)  # 2 corresponds to critical urgency
        }   
        # hints = {}
        notification_id = self.proxy.Notify(
            "", timer.notification_id, notification.icon, title,
            body,
            [], hints, 8000
        )
        print(f"notification sent with id {notification_id}", flush=True)
        threading.Thread(target=play_sound).start()
        # play_sound()

        #if timer:
            #print(f"id added {notification_id}", flush=True)
        if not ignore:
            timer.notification_id = notification_id

    def startTimer(self, interval, name):
        timer = Timer(interval, name, self.onTimerTimeout)
        self.timers.append(timer)

        title = f"{'Timer Started '}"
        body = f"Will Time out at {strftime('%X', localtime(timer.end))}"
        self.SendNotification(title, body, timer=timer, ignore=True)

    def deleteTimer(self, timer):
        self.timers.remove(timer)
        timer.cancel()

    def on_notification_closed(self, notification_id, reason):
        #print(f"notification closed with reason {reason} and id {notification_id}", flush=True)

        for timer in self.timers:
            if hasattr(timer, 'notification_id') and timer.notification_id == notification_id:
                if reason == 2:  # Reason 2 indicates a user action
                    print("self close", flush=True)
                    self.deleteTimer(timer)
                break

    def onTimerTimeout(self, timer):
        title = f"{timer.name if timer.name else 'Time is up'}"
        #print(f"timeout, {title}", flush=True)
        body = f"Timed out at {strftime('%X', localtime(timer.end))}"
        self.SendNotification(title, body, urgency='critical', timer=timer)
        self.schedule_resend(timer)

    def schedule_resend(self, timer):
        if timer in self.timers:
            timer.count += 1
            threading.Timer(10, self.resendNotification, [timer]).start()

    def resendNotification(self, timer):
        if timer in self.timers:
            title = f"{timer.name if timer.name else 'Reminder'} ({timer.count})"
            body = f"Reminder for timer named '{timer.name}'"
            self.SendNotification(title, body, urgency='critical', timer=timer)
            self.schedule_resend(timer)


    def getTimeDifference(self, localtime_var):

        # Assuming localtime_var is the given localtime variable
        # localtime_var = time.localtime(time.mktime(time.strptime("2025-01-15 10:00:00", "%Y-%m-%d %H:%M:%S")))

        # Get the current time
        current_time = localtime()

        # Convert both localtime structures to datetime objects
        localtime_dt = datetime(*localtime_var[:6])
        current_time_dt = datetime(*current_time[:6])

        # Calculate the difference
        time_difference = localtime_dt - current_time_dt

        # Extract hours and minutes from the difference
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes = remainder // 60
        seconds = remainder % 60

        # Format the difference
        formatted_difference = ""
        if hours > 0:
            formatted_difference += f"{int(hours)}h"
        if minutes > 0:
            formatted_difference += f"{int(minutes)}m"
        if seconds > 0:
            formatted_difference += f"{int(seconds)}s"
    
        # formatted_difference = f"{hours}h{minutes}m{seconds}s"
        return formatted_difference
        # #print(f"The given time is {formatted_difference} ahead of the current time.")
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
            # #print(f"{timer_name_with_quotes} ??", flush=True)
            remaining = self.getTimeDifference(localtime(timer.end))
            # #print(f"{remaining} ??", flush=True)

                                          
            items.append(StandardItem(
                id=self.name,
                text='Delete timer %s [%s]' % (timer_name_with_quotes, identifier),
                # subtext="Times out %s" % strftime("%X", localtime(timer.end)),
                subtext="Times out in %s" % remaining,
                iconUrls=self.iconUrls,
                actions=[Action("delete-timer", "Delete timer", lambda t=timer: self.deleteTimer(t))]
            ))

        if items:
            query.add(items)