from shared_libraries.helper_scripts import consulHelper, misc
import argparse 
from datetime import datetime
from plyer import notification
import os, sys, time
from shared_libraries.helper_scripts.mibianLib import mibian
import math

def notif(title, body):
      notification.notify(
        title = title,
        message = body,
        app_icon = "alert",
        timeout = 10,
    )

def maxLoss():
    return consulHelper.getConsulVar('shoonya/maxLoss')
    

def tradeCount():
    return consulHelper.getConsulVar('shoonya/tradeCount')
     
def killswitch(pnl, peakPnl, tradeCount, maxLoss):
    starttime = datetime.today().replace(hour=9, minute=15, second=0, microsecond=0)
    endtime = datetime.today().replace(hour=15, minute=30, second=0, microsecond=0)
    # endtime = datetime.today().replace(hour=23, minute=59, second=0, microsecond=0)

    current_date = datetime.today().strftime('%d-%m-%y')
    consul_date = consulHelper.getConsulVar('shoonya/date')

    if datetime.today() > starttime and datetime.today() < endtime:

    # shut down if max loss crossed
        if current_date == consul_date and pnl < maxLoss* -1:
                notif("max loss crossed", 'shutting down')
                time.sleep(5)
                # print('hui hui')
                os.system('systemctl poweroff') 

        # shut down if max pnl gets eroded
        if peakPnl >= 3000 and pnl <= peakPnl / 2:
            notif("max profit eroded", 'shutting down')
            time.sleep(5)
            os.system('systemctl poweroff') 

        # shut down if max trades crossed
        if tradeCount > 10:
            # notif("Too many trades", 'limit trading now')
            if tradeCount > 40 and pnl < 1000 :
                notif("trades exceeded 20", 'stopping trading now')
                time.sleep(5)
                os.system('systemctl poweroff') 


def pnl():
    pnl = consulHelper.getConsulVar('shoonya/pnl')
    peakPnl = consulHelper.getConsulVar('shoonya/peakPnl')
    tradeCount = consulHelper.getConsulVar('shoonya/tradeCount')
    if pnl != None:
        maxxLoss = consulHelper.getConsulVar('shoonya/maxLoss')
        killswitch(float(pnl), float(peakPnl), int(tradeCount),  float(maxxLoss))
    return pnl


def latestCE():
    latestCE = consulHelper.getConsulVar('shoonya/ceOtm')
    return latestCE

def latestPE():
    latestPE = consulHelper.getConsulVar('shoonya/peOtm')
    return latestPE

def checkValidDay():
    consul_date = consulHelper.getConsulVar('shoonya/date')
    if consul_date != datetime.now().strftime('%d-%m-%y'):
        print('NA')
        exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--getMaxLoss', action='store_true', default=None)
    parser.add_argument('--getPnl', action='store_true', default=None)
    parser.add_argument('--getTradeCount', action='store_true', default=None)
    parser.add_argument('--getLatestCE', action='store_true', default=None)
    parser.add_argument('--getLatestPE', action='store_true', default=None)

    args = parser.parse_args()

    checkValidDay()

    if args.getMaxLoss is not None:
        print(maxLoss())

    if args.getPnl is not None:
        print(pnl())

    if args.getTradeCount is not None:
        print(tradeCount())

    if args.getLatestCE is not None:
        print(latestCE())

    if args.getLatestPE is not None:
        print(latestPE())