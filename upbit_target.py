import pyupbit
import numpy as np
import matplotlib.pyplot as plt

def get_hpr(ticker):
        try:
            df = pyupbit.get_ohlcv(ticker)

            df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
            df['range'] = (df['high'] - df['low']) * 0.5
            df['target'] = df['open'] + df['range'].shift(1)
            df['bull'] = df['open'] > df['ma5']
            df['jhonber'] = df['open'] / df['open'][0]

            fee = 0.05 / 100
            df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                                   df['close'] / df['target'] - fee,
                                   1)

            df['hpr'] = df['ror'].cumprod()
            df['dd'] = (df['hpr'] / df['hpr'].cummax() - 1) * 100
            df['mdd'] = df['dd'].cummin()

            test(df)
            df.to_excel('test.xlsx')
            return df['hpr'][-2]

        except:
             return 1

def test(df):
    plt.figure(figsize=(9, 7))
    plt.subplot(211)
    df['jhonber'].plot(label='BTC', title='BTC MDD', grid=True, legend=True)
    df['hpr'].plot(c='blue', label='BTC hpr', grid=True, legend=True)
    plt.subplot(212)
    df['dd'].plot(c='gray', label='BTC dd', grid=True, legend=True)
    df['mdd'].plot(c='red', label='mdd', grid=True, legend=True)
    plt.show()

df = get_hpr("KRW-BTC")
print(df)