import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from mplfinance.original_flavor import candlestick2_ohlc
import pandas as pd
import numpy as np
import copy

from p407_gui.module.gathering import Gathering
from p407_gui.module import indicator


def draw_macd(df, fast_period, slow_period, signal_period, price):
    copy_df = copy.deepcopy(df)
    copy_df.reset_index(inplace=True)

    indicator.add_MACD(copy_df, fast_period, slow_period, signal_period, price)

    # x-축 날짜
    xdate = copy_df.Date.astype('str')
    for i in range(len(xdate)):
        xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

    # def mydate(x, pos):
    #     try:
    #         return xdate[int(x-0.5)]
    #     except IndexError:
    #         return ''

    # 차트 레이아웃 설정
    fig = plt.figure(figsize=(15, 15))
    ax_main = plt.subplot2grid((5, 1), (0, 0), rowspan=3)
    ax_sub = plt.subplot2grid((5, 1), (3, 0))
    ax_sub2 = plt.subplot2grid((5, 1), (4, 0))

    # ax_main 메인차트
    ax_main.set_title('Stock Chart', fontsize=20)
    ax_main.plot(xdate, copy_df['close'], 'k-')
    candlestick2_ohlc(ax_main, copy_df['open'], copy_df['high'],
                      copy_df['low'], copy_df['close'], width=0.6, colorup='r', colordown='b')

    # ax_sub 에 MACD 지표를 출력
    ax_sub.set_title('MACD', fontsize=15)
    # copy_df['macd_' + str(fast_period) + '_' + str(slow_period) + '_' + str(signal_period)].iloc[0] = 0
    ax_sub.plot(xdate, copy_df['macd_' + str(fast_period) + '_' + str(slow_period) + '_' + str(signal_period)], label='MACD')
    ax_sub.plot(xdate, copy_df['macd_signal_' + str(fast_period) + '_' + str(slow_period) + '_' + str(signal_period)], label='MACD Signal')
    ax_sub.legend(loc='best')

    # ax_sub2 에 MACD 오실레이터를 bar 차트로 출력
    ax_sub2.set_title('MACD Oscillator', fontsize=15)
    oscillator = copy_df['macd_hist_' + str(fast_period) + '_' + str(slow_period) + '_' + str(signal_period)]
    # oscillator.iloc[0] = 1e-16
    ax_sub2.bar(list(xdate), list(oscillator.where(oscillator > 0)), 0.7)
    ax_sub2.bar(list(xdate), list(oscillator.where(oscillator < 0)), 0.7)

    # x 축 조정
    ax_main.xaxis.set_major_locator(ticker.MaxNLocator(25))
    # ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    ax_sub.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_sub2.xaxis.set_major_locator(ticker.MaxNLocator(25))
    fig.autofmt_xdate()

    # 차트끼리 충돌을 방지합니다.
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


if __name__ == "__main__":

    mod = Gathering()
    df = mod.get_stock('000660', '2020-01-01', '2021-01-01', 'D')

    draw_macd(df, 12, 26, 9, 'close')