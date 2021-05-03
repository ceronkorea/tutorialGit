import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", count=200)
# print(df.head())

window = 252
peak = df['close'].rolling(window, min_periods=1).max()
drawdown = df['close'] / peak - 1.0
max_dd = drawdown.rolling(window, min_periods=1).min()

max_dd_min = max_dd.min()
print(max_dd_min)
print(max_dd[max_dd == max_dd_min])


import matplotlib.pyplot as plt
plt.figure(figsize=(9, 7))
plt.subplot(211)
df['close'].plot(label='BTC', title='BTC MDD', grid=True, legend=True)
plt.subplot(212)
drawdown.plot(c='blue', label='BTC DD', grid=True, legend=True)
max_dd.plot(c='red', label='BTC MDD', grid=True, legend=True)
plt.show()