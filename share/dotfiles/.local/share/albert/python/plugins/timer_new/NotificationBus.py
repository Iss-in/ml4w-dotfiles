from dasbus.loop import EventLoop
loop = EventLoop()

from dasbus.connection import SessionMessageBus
bus = SessionMessageBus()

proxy = bus.get_proxy(
    "org.freedesktop.Notifications",
    "/org/freedesktop/Notifications"
)

def callback(id, reason):
    print("The notification {} was closed.".format(id))

proxy.NotificationClosed.connect(callback)
loop.run()