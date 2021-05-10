import pyupbit
import pandas as pd
import datetime

today = datetime.datetime.now()
print(today)
print(type(today))
strtoday = today.strftime('%Y%m%d')
print(strtoday)
print(type(strtoday))




df = pyupbit.get_ohlcv("KRW-BTC", to=strtoday, count=3)

print(df)