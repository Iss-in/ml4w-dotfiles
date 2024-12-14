import os, sys, time
import math
import yaml
import json
import argparse 


from datetime import datetime
from shared_libraries.helper_scripts import consulHelper, misc
from shared_libraries.helper_scripts.mibianLib import mibian


config_file = "shared_libraries/config.yaml"
with open(config_file) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

bar_output = "{\"text\": \"text\", \"alt\": \"alt\", \"tooltip\": \"tooltip\", \"class\": \"shoonya\", \"percentage\": \"percentage\" }"

MAX_TRADES = 15 
MAX_TRADES_HARD = 40 

MAX_DRAWDOWN = 6000

def validTime():
    
    starttime = datetime.today().replace(hour=9, minute=0, second=0, microsecond=0)
    endtime = datetime.today().replace(hour=15, minute=30, second=0, microsecond=0)
    # endtime = datetime.today().replace(hour=23, minute=59, second=0, microsecond=0)

    session_status = consulHelper.getConsulVar('shoonya/endSession')
    if session_status == '1':
        # print(f"session status is {session_status}1")
        return False

    if datetime.today() > starttime and datetime.today() < endtime:
        return True
    return False


def maxLoss():
    return consulHelper.getConsulVar('shoonya/maxLoss')

def tradeCount():
    return consulHelper.getConsulVar('shoonya/tradeCount')

def endSession():
    consulHelper.setConsulVar('shoonya/endSession', 1)
    os.system('systemctl poweroff')

def killswitch(pnl, peakPnl, tradeCount, maxLoss):
    if validTime():
        current_date = datetime.today().strftime('%d-%m-%y')
        consul_date = consulHelper.getConsulVar('shoonya/date')

        shutdown=0
        # shut down if max loss crossed
        if current_date == consul_date and pnl < maxLoss* -1:
            misc.sendNotif(config,"max loss crossed", 'shutting down')
            shutdown=1
        # shut down if max pnl gets eroded
        if peakPnl >= MAX_DRAWDOWN and pnl <= peakPnl / 2:
            misc.sendNotif(config,"max profit eroded", 'shutting down')
            shutdown=1
        # shut down if max trades crossed
        if tradeCount > MAX_TRADES and pnl < 1000:
            misc.sendNotif(config,"Too many trades", 'limit trading now')
            shutdown=1
            
        
        if shutdown == 1:
            endSession()


def getPnl():
    pnl = consulHelper.getConsulVar('shoonya/pnl')
    peakPnl = consulHelper.getConsulVar('shoonya/peakPnl')
    tradeCount = consulHelper.getConsulVar('shoonya/tradeCount')
    if pnl != None:
        maxxLoss = consulHelper.getConsulVar('shoonya/maxLoss')
        killswitch(float(pnl), float(peakPnl), int(tradeCount),  float(maxxLoss))
    return round(int(pnl),1)


def getLatestCE():
    latestCE = consulHelper.getConsulVar('shoonya/ceOtm')
    return latestCE

def getLatestPE():
    latestPE = consulHelper.getConsulVar('shoonya/peOtm')
    return latestPE

# fix this
def checkValidDay():
    global bar_output
    current_date = datetime.now().strftime('%d-%m-%y')
    consul_date = consulHelper.getConsulVar('shoonya/date')
    if consul_date != current_date or misc.isValidDay(current_date) == False:
    # if consul_date != current_date :
        bar_output = bar_output.replace(": \"text",": \"")
        # print(consul_date, current_date)
        print(bar_output)
        exit(0)


def getBarInfo():
    global bar_output
    output = ""
    # if validTime():
    if True:
        trades = tradeCount()
        pnl = getPnl()
        output = f"trades: {trades}   pnl: {pnl}"
    # bar_output = f'{{\"text\":\"{output}\",\"alt\":\"123\",\"tooltip\":\" deets\",\"class\":\"shoonya\"}}'
    # return json.loads(bar_output)
    # bar_output = output + "\n" + "trading details" + "\n" + "shoonya"'
    return bar_output.replace(": \"text",": \""+output)
    # print(bar_output)
    # return bar_output


def getBarInfoOption():
    global bar_output
    output = ""
    if validTime():
    # if True:        
        # print(f"valid time", flush=True)
        latestCE = getLatestCE()
        latestPE = getLatestPE()
        output = f"{latestCE} {latestPE}"
    # bar_output = f'{{\"text\":\"{output}\",\"alt\":\"123\",\"tooltip\":\" deets\",\"class\":\"shoonya\"}}'
    # return json.loads(bar_output)
    # bar_output = output + "\n" + "trading details" + "\n" + "shoonya"'
    return bar_output.replace(": \"text",": \""+output)
    # print(bar_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--getMaxLoss', action='store_true', default=None)
    parser.add_argument('--getPnl', action='store_true', default=None)
    parser.add_argument('--getTradeCount', action='store_true', default=None)
    parser.add_argument('--getLatestCE', action='store_true', default=None)
    parser.add_argument('--getLatestPE', action='store_true', default=None)
    parser.add_argument('--getBarInfo', action='store_true', default=None)
    parser.add_argument('--getBarInfoOption', action='store_true', default=None)

    args = parser.parse_args()

    # checkVadlidDay()

    if args.getMaxLoss is not None:
        print(maxLoss())

    if args.getPnl is not None:
        print(getPnl())

    if args.getTradeCount is not None:
        print(tradeCount())

    if args.getLatestCE is not None:
        print(getLatestCE())

    if args.getLatestPE is not None:
        print(getLatestPE())

    if args.getBarInfo is not None:
        print(getBarInfo())

    if args.getBarInfoOption is not None:
        print(getBarInfoOption())