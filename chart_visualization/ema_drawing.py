import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from mplfinance.original_flavor import candlestick2_ohlc
import pandas as pd
import copy
import csv

from p407_gui.module import indicator
from p407_gui.module.gathering import Gathering


def draw_ema(df, period, price):
    copy_df = copy.deepcopy(df)
    copy_df.reset_index(inplace=True)

    indicator.add_EMA(copy_df, period, price)

    # 한글 폰트 지정
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    fig, ax = plt.subplots(figsize=(12, 10))

    # x-축 날짜
    xdate = copy_df.Date.astype('str')
    for i in range(len(xdate)):
        xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

    ax.plot(xdate, copy_df['ema_'+str(period)], 'g-', label='EMA'+str(period))
    ax.plot(xdate, copy_df[price], 'k-')
    candlestick2_ohlc(ax, copy_df['open'], copy_df['high'],
                      copy_df['low'], copy_df['close'], width=0.6, colorup='r', colordown='b')

    ax.set_title('Stock Chart', fontsize=20)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax.legend(loc='best') # legend 위치

    plt.xticks(rotation=45)  # x-축 글씨 45도 회전
    plt.grid()  # 그리드 표시
    plt.show()


if __name__ == "__main__":

    mod = Gathering()
    df = mod.get_stock('000660', '2020-01-01', '2021-01-01', 'D')

    # print(df)
    draw_ema(df, 30, 'close')