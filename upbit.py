#참고링크:https://wikidocs.net/31063

#설치
#pip install pyupbit
#pip install -U pyupbit

import pyupbit
import time
import json
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

import datetime

def dateToStr(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")

def strToDate(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

def loadData(date):
    data = pyupbit.get_ohlcv("KRW-BTC", interval="days", count=100, to=dateToStr(date))
    #data = pyupbit.get_ohlcv("KRW-MBL", interval="minute1", count=12, to=dateToStr(date))
    #data = pyupbit.get_ohlcv("KRW-MBL", interval="minute1")
    return data

date = datetime.datetime.now()

data = loadData(date)



list = []
while True:
    data = loadData(date)

    for i in reversed(range(0, len(data))):
        #open, high, low, close
        if i == 0 and len(data) >= 100:
            break
        if data.index[i] < strToDate("2019-08-01 09:00:00"):
            break
        str = "{0}\t{1}\t{2}\t{3}\t{4}".format(data.index[i].strftime("%Y-%m-%d"), data.open[i], data.high[i], data.low[i], data.close[i])
        list.append(str)
    if len(data) >= 100:
        date = data.index[0]
        time.sleep(0.1)
    else:
        break
list.reverse()
for i in range(0, len(list)):
    print(list[i])

