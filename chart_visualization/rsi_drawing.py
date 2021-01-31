import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from mplfinance.original_flavor import candlestick2_ohlc
import pandas as pd
import copy

from p407_gui.module import indicator
from p407_gui.module.gathering import Gathering

def draw_rsi(df, period, price):
    copy_df = copy.deepcopy(df)
    copy_df.reset_index(inplace=True)

    indicator.add_RSI(copy_df, period, price)

    # x-축 날짜
    xdate = copy_df.Date.astype('str')
    for i in range(len(xdate)):
        xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

    # 차트 레이아웃 설정
    fig = plt.figure(figsize=(15, 15))
    ax_main = plt.subplot2grid((5, 1), (0, 0), rowspan=3)
    ax_sub = plt.subplot2grid((5, 1), (3, 0))

    # ax_main 메인차트
    ax_main.set_title('Stock Chart', fontsize=20)
    ax_main.plot(xdate, copy_df['close'], 'k-')
    candlestick2_ohlc(ax_main, copy_df['open'], copy_df['high'],
                      copy_df['low'], copy_df['close'], width=0.6, colorup='r', colordown='b')
    ax_main.set_xlabel('Date')
    ax_main.set_ylabel("Price")

    # ax_sub에 rsi 차트 그림
    ax_sub.set_title('RSI', fontsize=15)
    # copy_df['rsi_'+str(period)].iloc[0] = 0
    ax_sub.plot(xdate, copy_df['rsi_'+str(period)], label='rsi' + str(period))
    ax_sub.set_xlabel('Date')
    ax_sub.set_ylabel("Price")
    ax_sub.legend(loc='best')

    # x 축 조정
    ax_main.xaxis.set_major_locator(ticker.MaxNLocator(25))
    ax_sub.xaxis.set_major_locator(ticker.MaxNLocator(25))

    # 차트 간 충돌 방지
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


if __name__ == "__main__":

    mod = Gathering()
    df = mod.get_stock('000660', '2020-01-01', '2021-01-01', 'D')

    draw_rsi(df, 30, 'close')