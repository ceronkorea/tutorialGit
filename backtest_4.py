# 참고링크:https://wikidocs.net/31063

# 설치
# pip install pyupbit
# pip install -U pyupbit

import pandas as pd
import pyupbit
import time
import json
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


import datetime


def dateToStr(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


def strToDate(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")


def loadData(str, date):
    data = pyupbit.get_ohlcv(str, interval="days", count=100, to=dateToStr(date))
    return data



dic = {}

def initData(type):
    ar_index = []
    ar_open = []
    ar_high = []
    ar_low = []
    ar_close = []
    #date = datetime.datetime.now()
    date = datetime.datetime.now() - datetime.timedelta(days=2)
    while True:
        data = loadData(type, date)
        for i in reversed(range(0, len(data))):
            # open, high, low, close
            if data.index[i] < strToDate("2019-09-13 09:00:00"):
                break
            ar_index.append(data.index[i])
            ar_open.append(data.open[i])
            ar_high.append(data.high[i])
            ar_low.append(data.low[i])
            ar_close.append(data.close[i])
        if len(data) >= 100:
            date = data.index[0]
            time.sleep(0.1)
        else:
            break
    ar_index.reverse()
    ar_open.reverse()
    ar_high.reverse()
    ar_low.reverse()
    ar_close.reverse()

    dic[type] = {
        "index" : ar_index,
        "open" : ar_open,
        "high" : ar_high,
        "low" : ar_low,
        "close" : ar_close
    }

#list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-BCH", "KRW-LTC"]
#list = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-XRP"]
list = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-BSV"]
initData(list[0])
initData(list[1])
initData(list[2])
initData(list[3])


def func1():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    for ii in range(len(list)):
        dic_value[list[ii]] = 1 / len(list)
    for i in range(1, index_len):
        value = 0
        for ii in range(len(list)):
            type = list[ii]
            dic_value[type] *= dic[type]["open"][i] / dic[type]["open"][i-1]
            value += dic_value[type]
        print("{0:0.6f}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}".format(dic_value[list[0]], dic_value[list[1]],
                                                                  dic_value[list[2]], dic_value[list[3]]))

        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)
    CAGR = pow(value, (365 / index_len)) - 1
    print("매수후보유")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func2(count_max):
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    count = count_max
    for i in range(index_len):
        #print(dic[list[0]]["index"][i])
        if count >= count_max:
            for ii in range(len(list)):
                type = list[ii]
                dic_value[type] = value / len(list)
            count = 0
        count += 1
        print("{0:0.6f}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}".format(dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value = 0
        for ii in range(len(list)):
            type = list[ii]
            dic_value[type] *= dic[type]["close"][i] / dic[type]["open"][i]
            value += dic_value[type]
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)
    CAGR = pow(value, (365 / index_len)) - 1
    print("리벨런싱")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func3():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    k = 0.5
    fee = 0.0005
    for ii in range(len(list)):
        dic_value[list[ii]] = 1 / len(list)
    for i in range(1, index_len-1):
        value = 0
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i-1] - dic[type]["low"][i-1]
            price_buy = dic[type]["open"][i] + _range * k
            rate = 0
            if dic[type]["high"][i] > price_buy:
                price_sell = dic[type]["open"][i+1]
                rate = (price_sell*(1-fee))/(price_buy*(1+fee))-1
                dic_value[type] = dic_value[type] * (1 + rate)

            value += dic_value[type]
        print("{0:0.6f}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}".format(dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value/value_max-1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("변동성돌파")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()


def func4():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    k = 0.5
    fee = 0.0005
    count_max = 2
    count = count_max
    for ii in range(len(list)):
        dic_value[list[ii]] = 1 / len(list)
    for i in range(1, index_len-1):
        #print(dic[list[0]]["index"][i])
        if count >= count_max:
            for ii in range(len(list)):
                type = list[ii]
                dic_value[type] = value / len(list)
            count = 0
        count += 1

        value = 0
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i-1] - dic[type]["low"][i-1]
            price_buy = dic[type]["open"][i] + _range * k
            rate = 0
            if dic[type]["high"][i] > price_buy:
                price_sell = dic[type]["open"][i+1]
                rate = (price_sell*(1-fee))/(price_buy*(1+fee))-1
                dic_value[type] = dic_value[type] * (1 + rate)

            value += dic_value[type]
        print("{0}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}\t{4:0.6f}".format(dic[list[0]]["index"][i+1].strftime("%Y-%m-%d"), dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value/value_max-1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("변동성돌파리벨")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func4_2():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    k = 0.5
    fee = 0.0005
    count_max = 2
    count = count_max
    for ii in range(len(list)):
        dic_value[list[ii]] = 1 / len(list)
    for i in range(1, index_len-1):
        #print(dic[list[0]]["index"][i])
        if count >= count_max:
            for ii in range(len(list)):
                type = list[ii]
                dic_value[type] = value / len(list)
            count = 0
        count += 1

        value = 0
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i-1] - dic[type]["low"][i-1]
            price_buy = dic[type]["open"][i] + _range * k
            rate = 0
            isOver = dic[type]["open"][i] > (dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
            isBuy = dic[type]["high"][i] > price_buy
            if isOver and isBuy:
                price_sell = dic[type]["open"][i+1]
                rate = (price_sell*(1-fee))/(price_buy*(1+fee))-1
                dic_value[type] = dic_value[type] * (1 + rate)

            value += dic_value[type]
        print("{0}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}\t{4:0.6f}".format(dic[list[0]]["index"][i+1].strftime("%Y-%m-%d"), dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value/value_max-1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("추세변동성돌파리벨")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func5():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    dic_isOver_prev = {}
    dic_price_buy = {}
    fee = 0.0005
    count_max = 2
    count = count_max
    for ii in range(len(list)):
        type = list[ii]
        dic_value[type] = 1 / len(list)
        dic_isOver_prev[type] = False
        dic_price_buy[type] = 0
    for i in range(2, index_len):
        value = 0
        #print(dic[list[0]]["index"][i])
        for ii in range(len(list)):
            type = list[ii]

            isOver = dic[type]["open"][i] > (dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
            isBuy = (dic_isOver_prev[type] == False and isOver == True)
            isSell = (dic_isOver_prev[type] == True and isOver == False)
            dic_isOver_prev[type] = isOver
            if isBuy:
                dic_price_buy[type] = dic[type]["open"][i]
            if isSell:
                price_sell = dic[type]["open"][i]
                rate = (price_sell * (1 - fee)) / (dic_price_buy[type] * (1 + fee)) - 1
                dic_value[type] = dic_value[type] * (1 + rate)
            value += dic_value[type]
        print("{0:0.6f}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}".format(dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)




    CAGR = pow(value, (365 / index_len)) - 1
    print(value)
    print(index_len)
    print("추세")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()


def func6(count_max):
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    dic_isOver_prev = {}
    dic_price_buy = {}
    fee = 0.0005
    count = count_max
    for ii in range(len(list)):
        type = list[ii]
        dic_value[type] = 1 / len(list)
        dic_isOver_prev[type] = False
        dic_price_buy[type] = 0
    for i in range(2, index_len):
        #print(dic[list[0]]["index"][i])
        if count >= count_max:
            for ii in range(len(list)):
                type = list[ii]
                dic_value[type] = value / len(list)
            count = 0
        count += 1
        value = 0
        for ii in range(len(list)):
            type = list[ii]

            isOver = dic[type]["open"][i] > (
                        dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
            isBuy = (dic_isOver_prev[type] == False and isOver == True)
            isSell = (dic_isOver_prev[type] == True and isOver == False)
            dic_isOver_prev[type] = isOver
            if isBuy:
                dic_price_buy[type] = dic[type]["open"][i]
            if isSell:
                price_sell = dic[type]["open"][i]
                rate = (price_sell * (1 - fee)) / (dic_price_buy[type] * (1 + fee)) - 1
                dic_value[type] = dic_value[type] * (1 + rate)
            value += dic_value[type]
        print("{0:0.6f}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}".format(dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("추세리벨런싱")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func7():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    dic_isOver_prev = {}
    dic_price_buy = {}
    k = 0.5
    fee = 0.0005
    for ii in range(len(list)):
        type = list[ii]
        dic_value[type] = 1 / len(list)
        dic_isOver_prev[type] = False
        dic_price_buy[type] = 0
    for i in range(2, index_len):
        value = 0
        #print(dic[list[0]]["index"][i])
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i - 1] - dic[type]["low"][i - 1]
            _price_buy = dic[type]["open"][i] + _range * k
            isOver1 = dic[type]["high"][i] > _price_buy
            isOver2 = dic[type]["open"][i] > (dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
            isOver = isOver1 and isOver2
            isBuy = (dic_isOver_prev[type] == False and isOver == True)
            isSell = (dic_isOver_prev[type] == True and isOver == False)
            dic_isOver_prev[type] = isOver

            if isBuy:
                dic_price_buy[type] = _price_buy
            if isSell:
                price_sell = dic[type]["open"][i + 1]
                rate = (price_sell * (1 - fee)) / (dic_price_buy[type] * (1 + fee)) - 1
                dic_value[type] = dic_value[type] * (1 + rate)
                #if ii == 3:
                    #print("{0} \t {1} \t {2:0.2f}% \t {3:0.6f}".format(dic_price_buy[type], price_sell, rate*100, dic_value[type]*5))
            value += dic_value[type]
        print("{0}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}\t{4:0.6f}".format(dic[list[0]]["index"][i+1].strftime("%Y-%m-%d"), dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("추세변돌대기")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func8():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    dic_isResult_prev = {}
    dic_price_buy = {}
    k = 0.5
    fee = 0.0005
    krw = 1
    count = 0
    count_max = 4
    for ii in range(len(list)):
        type = list[ii]
        dic_isResult_prev[type] = False
        dic_price_buy[type] = 0
        dic_value[type] = 0
    for i in range(2, index_len):
        #print(dic[list[0]]["index"][i])
        value = 0
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i - 1] - dic[type]["low"][i - 1]
            _price_buy = dic[type]["open"][i] + _range * k
            isOver = dic[type]["high"][i] > _price_buy
            isBull = dic[type]["open"][i] > (dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
            isResult = (isBull and isOver) or (isBull and dic_isResult_prev[type])
            isBuy = (dic_isResult_prev[type] == False and isResult == True)
            isSell = (dic_isResult_prev[type] == True and isResult == False)
            dic_isResult_prev[type] = isResult

            #for test
            if i + 1 == index_len:
                isSell = True

            if isBuy:
                dic_price_buy[type] = _price_buy
                amount = krw * 1 / (count_max - count)
                dic_value[type] = amount
                krw -= amount
                count += 1
            if isSell:
                price_sell = dic[type]["open"][i]
                #print(dic_price_buy[type], price_sell)
                rate = (price_sell * (1 - fee)) / (dic_price_buy[type] * (1 + fee)) - 1
                krw += dic_value[type] * (1 + rate)
                dic_value[type] = 0
                count -= 1

            value += dic_value[type]
        value += krw
        print("{0}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}\t{4:0.6f}\t{5:0.6f}".format(dic[list[0]]["index"][i].strftime("%Y-%m-%d"), krw, dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("추세변돌대기리벨")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()

def func9():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    dd = 0
    mdd = 0
    CAGR = 0
    dic_value = {}
    dic_price_buy = {}
    dic_state = {}
    k = 0.5
    fee = 0.0005
    krw = 1
    count = 0
    count_max = 4
    for ii in range(len(list)):
        type = list[ii]
        dic_price_buy[type] = 0
        dic_value[type] = 0
        dic_state[type] = "ready"
    for i in range(2, index_len):
        #print(dic[list[0]]["index"][i])
        value = 0
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i - 1] - dic[type]["low"][i - 1]
            _price_buy = dic[type]["open"][i] + _range * k

            if dic_state[type] == "hold":
                isSell = dic[type]["open"][i] <= (dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
                if i + 1 == index_len:
                    isSell = True
                if isSell:
                    # isNotBull
                    dic_state[type] = "ready"
                    # sell
                    price_sell = dic[type]["open"][i]
                    rate = (price_sell * (1 - fee)) / (dic_price_buy[type] * (1 + fee)) - 1
                    krw += dic_value[type] * (1 + rate)
                    dic_value[type] = 0
                    count -= 1
                    #print("sell", type, price_sell, dic_price_buy[type], "{0:0.2f}%".format((price_sell/dic_price_buy[type]-1)*100))
            if dic_state[type] == "ready":
                isBuy = dic[type]["high"][i] > _price_buy
                if i + 1 == index_len:
                    isBuy = False
                if isBuy:
                    # isOver
                    dic_state[type] = "hold"
                    # buy
                    dic_price_buy[type] = _price_buy
                    amount = krw * 1 / (count_max - count)
                    dic_value[type] = amount
                    krw -= amount
                    count += 1
                    #print("buy", type, dic_price_buy[type])

            value += dic_value[type]
        value += krw
        print("{0}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}\t{4:0.6f}\t{5:0.6f}".format(dic[list[0]]["index"][i].strftime("%Y-%m-%d"), krw, dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("추세변돌대기2")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()


def func10():
    index_len = 0
    for i in range(len(list)):
        type = list[i]
        index_len = max(index_len, len(dic[type]["index"]))

    value = 1
    value_max = value
    mdd = 0
    dic_value = {}
    dic_price_buy = {}
    dic_state = {}
    k = 0.5
    fee = 0.0005
    krw = 1
    count = 0
    count_max = 4
    for ii in range(len(list)):
        type = list[ii]
        dic_price_buy[type] = 0
        dic_value[type] = 0
        dic_state[type] = "ready"
    for i in range(20, index_len):
        #print(dic[list[0]]["index"][i])
        value = 0
        for ii in range(len(list)):
            type = list[ii]
            _range = dic[type]["high"][i - 1] - dic[type]["low"][i - 1]

            _price_buy = dic[type]["open"][i] + _range * k

            if dic_state[type] == "hold":
                #시가가 3일 이동평균 이하면 매도
                isSell = dic[type]["open"][i] <= (dic[type]["open"][i - 2] + dic[type]["open"][i - 1] + dic[type]["open"][i]) / 3
                if i + 1 == index_len:
                    #마지막 날짜는 정산을 위해 백테스트시 강제매도
                    isSell = True
                if isSell:
                    # isNotBull
                    dic_state[type] = "ready"
                    # sell
                    price_sell = dic[type]["open"][i]
                    rate = (price_sell * (1 - fee)) / (dic_price_buy[type] * (1 + fee)) - 1
                    krw += dic_value[type] * (1 + rate)
                    dic_value[type] = 0
                    count -= 1
                    #print("sell", type, price_sell, dic_price_buy[type], "{0:0.2f}%".format((price_sell/dic_price_buy[type]-1)*100))

            #elif를 안쓰는 이유 : 시가에 매도 후에 돌파하면 재매수

            if dic_state[type] == "ready":
                #변동성돌파시 매수
                isBuy = dic[type]["high"][i] > _price_buy
                if i == index_len - 1:
                    isBuy = False
                if isBuy:
                    momentum = 0
                    #3일 이동평균 부터 20일 이동평균 구하기
                    for j in range(3, 20 + 1):
                        ma = 0
                        for jj in range(1, j + 1):
                            ma += dic[type]["close"][i - jj]
                        ma /= j
                        if ma < dic[type]["open"][i]:
                            momentum += 1
                            #모멘텀 점수 (최소:0점, 최대:18점)
                    momentum = momentum / 18 # 0 ~ 1 사이 값으로 변환

                    if momentum == 0:
                        continue

                    # isOver
                    dic_state[type] = "hold"
                    # buy
                    dic_price_buy[type] = _price_buy

                    amount = krw * 1 / (count_max - count) * momentum
                    # count : 매수 후 보유중인 가상화폐 개수
                    # count_max : 가상화폐 전체 개수
                    # 1 / (count_max - count) : N빵 투자 (count 0개 = 1/4, count 1개 = 1/3,  count 2개 = 1/2, count 3개 = 1/1)
                    # momentum : 모멘텀 값이 높을 수록 비중을 많이, 낮을수록 적게
                    dic_value[type] = amount
                    krw -= amount
                    count += 1
                    #print("buy", type, dic_price_buy[type])

            value += dic_value[type]
        value += krw
        print("{0}\t{1:0.6f}\t{2:0.6f}\t{3:0.6f}\t{4:0.6f}\t{5:0.6f}".format(dic[list[0]]["index"][i].strftime("%Y-%m-%d"), krw, dic_value[list[0]], dic_value[list[1]], dic_value[list[2]], dic_value[list[3]]))
        value_max = max(value_max, value)
        dd = value / value_max - 1
        mdd = min(mdd, dd)

    CAGR = pow(value, (365 / index_len)) - 1
    print("변돌대기이평모멘텀")
    print("CAGR:{0:0.2f}%".format(CAGR * 100))
    print("MDD:{0:0.2f}%".format(mdd * 100))
    print()


#func1()
#func2(2)
#func3()
#func4() #
#func4_2()
#func5()
#func6(1)
#func7()
#func8() #
#func9()
# func10() #