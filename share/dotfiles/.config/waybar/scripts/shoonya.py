import os,sys
import yaml
import requests
from datetime import datetime

config_file = "/home/kushy/Syncthing/Projects/Shoonya/shared_libraries/config.yaml"
with open(config_file) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
consul_host = config['consul']['host']
# print(consul_host)

headers = {
    'Content-Type': 'application/json',
}

def getTrades():
    trades_req = requests.get(f"http://{consul_host}:8500/v1/kv/shoonya/tradeCount?raw", headers=headers, timeout=10)
    trades = trades_req.content.decode("utf-8")
    return trades

def getPnl():
    pnl_req = requests.get(f"http://{consul_host}:8500/v1/kv/shoonya/pnl?raw", headers=headers, timeout=10)
    pnl = pnl_req.content.decode("utf-8")
    return pnl
# for content in trades_req:

trades = getTrades()
pnl = getPnl()
output = f"trades: {trades}   pnl: {pnl}"


start_time = datetime.now().replace(hour=9,minute=15)
end_time = datetime.now().replace(hour=15,minute=40)
current_time = datetime.now()

if current_time >= start_time and current_time <= end_time:
    print(f"{{\"text\":\"{output}\",\"alt\":\"123\",\"tooltip\":\" deets\",\"class\":\"shoonya\"}}")

    if int(pnl) < -5000:
        os.system('systemctl poweroff')
