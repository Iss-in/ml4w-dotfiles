import os
import subprocess
import json
import signal




output = subprocess.check_output(["slurp", "-p"]) # shell=False
output = output.decode('utf-8').strip()
x,y = output.split(' ')[0].split(',')
x = int(x)
y = int(y)
print(f"coordinates are {x}, {y}")



output = subprocess.check_output(["hyprctl", "activeworkspace", "-j"])
output = output.decode('utf-8').strip()
workspace = json.loads(output)['id']
print(f"workspace is {workspace}")



output = subprocess.check_output(["hyprctl", "clients", "-j"]) # shell=False
output = output.decode('utf-8').strip()

window_list = []
windows = json.loads(output)
# windows.reverse()
for window in windows:
    a = window['at'][0]
    b = window['at'][1]
    c = a + window['size'][0]
    d = b + window['size'][1]
    w_workspace = window['workspace']['id']
    # print(a,b,c,d, window['initialTitle'])
    if x >= a and x <=c and y >=b and y <=d and workspace == w_workspace:
        # print(f"focussed window is {window['initialTitle']}") 
        window_list.append(window)
        pid = window['pid']
        # os.kill(pid, signal.SIGTERM)
        # exit(0)


sorted_array = sorted(
    window_list,
    key=lambda x: (-x['floating'], x['focusHistoryID'])  # Sort by 'floating', then 'focusid' in ascending order
)

for window in window_list:
    print(json.dumps(window, indent=2))
window = sorted_array[0]
print(f"focussed window is {window['initialTitle']}") 
pid = window['pid']
os.kill(pid, signal.SIGTERM)

# if len(window_list) == 1:
#     window = window_list[0]
#     print(f"single window")
#     pid = window['pid']
#     os.kill(pid, signal.SIGTERM)
# else:
#     for index, window in enumerate(window_list):
#         if index == len(window_list) -1 or window_list[index+1]['floating'] == False:
#             print(f"last window, killing it")
#         if window['floating'] == True and window_list[index+1]['floating'] == False:
#             print(f"killing floating window, next is tiling")
#         else:



# import json

# # Sample array of JSON objects
# json_array = [
#     {"floating": True, "focusid": 5},
#     {"floating": False, "focusid": 3},
#     {"floating": True, "focusid": 1},
#     {"floating": True, "focusid": 4},
#     {"floating": False, "focusid": 2},
# ]

# # Sort the JSON array
# sorted_array = sorted(
#     windows,
#     key=lambda x: (-x['floating'], x['focusid'])  # Sort by 'floating', then 'focusid' in ascending order
# )

# # Print the sorted array
# print(json.dumps(sorted_array, indent=2))