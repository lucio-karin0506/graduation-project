import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from mplfinance.original_flavor import candlestick2_ohlc
import pandas as pd
import numpy as np
import copy

from p407_gui.module.gathering import Gathering
from p407_gui.module import indicator


def draw_bband(df, period, nbdevup, nbdevdn, price):
    copy_df = copy.deepcopy(df)
    copy_df.reset_index(inplace=True)

    indicator.add_BBands(copy_df, period, nbdevup, nbdevdn, price)

    # x-축 날짜
    xdate = copy_df.Date.astype('str')
    for i in range(len(xdate)):
        xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

    # 차트 레이아웃 설정
    fig = plt.figure(figsize=(12, 10))
    ax_main = plt.subplot()

    # ax_main 메인차트
    ax_main.set_title('Stock Chart', fontsize=20)
    ax_main.plot(xdate, copy_df['ubb_' + str(period) + '_' + str(nbdevup) + '_' + str(nbdevdn)], label="Upper limit", linewidth=0.7, color='k')
    ax_main.plot(xdate, copy_df['mbb_' + str(period) + '_' + str(nbdevup) + '_' + str(nbdevdn)], label="center line", linewidth=0.7, color='y')
    ax_main.plot(xdate, copy_df['lbb_' + str(period) + '_' + str(nbdevup) + '_' + str(nbdevdn)], label="Lower limit", linewidth=0.7, color='k')
    candlestick2_ohlc(ax_main, copy_df['open'], copy_df['high'],
                      copy_df['low'], copy_df['close'], width=0.6, colorup='r', colordown='b')

    ax_main.legend(loc='best')

    # x 축 조정
    ax_main.xaxis.set_major_locator(ticker.MaxNLocator(25))
    fig.autofmt_xdate()

    # 차트 간 충돌 방지
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


if __name__ == "__main__":

    mod = Gathering()
    df = mod.get_stock('000660', '2020-01-01', '2021-01-01', 'D')

    draw_bband(df, 10, 2, 2, 'close')