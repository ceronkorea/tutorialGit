import pandas as pd
import pyupbit
import datetime
import time
import numpy as np

Init = 0
Loop = 1
End = 2

# 초기화 시작
Mode = Init

second = 0.2
count = 200

k = 0.5

# datetime을 str로 변환
def get_dfstrftime(df):
    return df.strftime('%Y%m%d')


dfList = []


def get_df_ohlcv(_toDay, _ticker="KRW-BTC", interval='day', _count=200):
    return pyupbit.get_ohlcv(_ticker, interval=interval, count=_count, to=_toDay)


while True:
    time.sleep(second)
    if Mode == End:
        break
    if Mode == Init:
        StrToday = get_dfstrftime(datetime.datetime.now())
        df = get_df_ohlcv(StrToday)
        dfList.append(df)

        # 수집 모드 시작
        Mode = Loop

    elif Mode == Loop:
        StartStrDay = df.index[0].strftime('%Y%m%d')
        df = get_df_ohlcv(StartStrDay)

        if len(df) > 0:
            dfList.append(df)
        else:
            # 마지막 데이터
            Mode = End

    else:
        break

CollectDf = pd.concat(dfList)
SortDf = CollectDf.sort_index(ascending=True)
print(SortDf.info())
SortDf['range'] = (SortDf['high'] - SortDf['low'] ) * k
SortDf['target'] = SortDf['open'] + SortDf['range'].shift(1)

SortDf.to_excel(get_dfstrftime(datetime.datetime.now()) + '.xlsx')

# SortDf = CollectDf.sort_index(ascending=True).to_csv(get_dfstrftime(datetime.datetime.now()) + '.csv')