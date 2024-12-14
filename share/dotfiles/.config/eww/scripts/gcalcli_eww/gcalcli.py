# %%
import subprocess
import json
from datetime import datetime, timedelta
import re 
import argparse
# Run the gcalcli command
current_date = datetime.now()
next_date = current_date + timedelta(days=1)
command = ["gcalcli", "--refresh" ,"agenda", current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'), "--details", "end"]
result = subprocess.run(command, capture_output=True, text=True)
command_update = ["/bin/eww", "update"]

# print(result)

# %%
gcalcli_output = str(result.stdout)
print(str(gcalcli_output))

# %%

def strip_ansi_colors(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# %%
date_str = datetime.now().strftime('%a %b %d') + ' '
print(date_str)
resultstr = strip_ansi_colors(gcalcli_output).replace(date_str, "", 1)


# %%
events = []
full_day_events = []
counter = 0
for line in resultstr.splitlines():
    line = line.lstrip()
    if ':' in line:
        match = re.match(r'(?P<start_time>\d{1,2}:\d{2}[ap]m)\s*-\s*(?P<end_time>\d{1,2}:\d{2}[ap]m)\s+(?P<title>.+)', line)
        start_time = match.group("start_time")
        end_time = match.group("end_time")
        title = match.group("title")
        event = {'start':start_time, 'end':end_time, 'title':title}
        # event = {'interval':f"{start_time}-{end_time}", 'title':title}

        events.append(event)
    elif line != '':
        full_day_events.append({counter:line})
        counter = counter + 1
        
print(events)
print(full_day_events)

# %%
def dt(time_str):
    time_obj =  datetime.strptime(time_str, '%I:%M%p').time()
    dt_obj =  datetime.combine(datetime.now().date(), time_obj)
    # print(dt_obj)
    return dt_obj

# %%


def get_events():
    current_event = ''
    next_event = {}

    current_time = datetime.now()
    for i, event in enumerate(events):
        if dt(event['start']) < current_time and dt(event['end']) >current_time:
            current_event = event
            if i < len(events) - 1:
                next_event = events[i+1]
            print(f"current event is {current_event}")
            print(f"next event is {next_event}")
            break
        elif dt(event['start']) > current_time:
            next_event = event
            print(f"no current event next event is {next_event}")
            break
    data = {'0':current_event ,'1': next_event}
    with open("/tmp/events.json", "w") as file:
        json.dump(data, file, indent=4) 
    with open("/tmp/entire_day_events.json", "w") as file:
        json.dump(full_day_events, file, indent=4) 

def getCurrentEvent():
    current_event, b = get_events()
    return current_event

def getNextEvent():
    a , next_event = get_events()
    return next_event
    

# %%
get_events()
result = subprocess.run(command_update, capture_output=True, text=True)


# %%
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--getCurrentEvent', action='store_true', default=None)
#     parser.add_argument('--getNextEvent', action='store_true', default=None)
    
#     args = parser.parse_args()


#     if args.getCurrentEvent is not None:
#         print(getCurrentEvent())

#     if args.getNextEvent is not None:
#         print(getNextEvent())


