import platform
import PySide2
import sys
import os
import copy
import pandas as pd
import numpy as np

from PySide2.QtGui import *
from PySide2.QtWidgets import *

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from matplotlib.figure import Figure
from matplotlib import style
from p407_gui.interface.tech_indi_param_dialog import ma_dialog

from mplfinance.original_flavor import candlestick2_ohlc

class basic_drawing():
    # Draw graph 버튼 누를 때 그래프 차트 그리는 함수
    def basic_d_graph(self, path):
        df = pd.read_csv(path, index_col=0, parse_dates=[0], encoding='cp949')
        copy_df = copy.deepcopy(df)
        copy_df.reset_index(inplace=True)

        # 한글 폰트 지정
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)

        # x-축 날짜
        xdate = copy_df.Date.astype('str')
        for i in range(len(xdate)):
            xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

        self.axes[0].plot(xdate, copy_df['close'], linewidth=0.1, color='k')
        candlestick2_ohlc(self.axes[0], copy_df['open'], copy_df['high'], copy_df['low'], copy_df['close'],
                                width=0.5, colorup='r', colordown='b')

        self.fig.suptitle("stock chart")
        self.fig.autofmt_xdate(rotation=45)
        self.axes[0].set_xlabel("Date")
        self.axes[0].set_ylabel("Price")
        self.axes[0].xaxis.set_major_locator(ticker.MaxNLocator(25))
        self.axes[0].legend(loc='best')  # legend 위치
        self.axes[0].grid()
        # self.axes[0].set_xticks(xticks)
        # self.axes[0].set_xticklabels(xlabels, rotation=45, minor=False)

        scale = 1.1
        self.zoom_factory(self.axes[0], base_scale=scale)
        self.pan_factory(self.axes[0])

        self.draw()

    def basic_w_graph(self, path):
        df = pd.read_csv(path, index_col=0, parse_dates=[0], encoding='cp949')
        copy_df = copy.deepcopy(df)
        copy_df.reset_index(inplace=True)

        # 한글 폰트 지정
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)

        # x-축 날짜
        xdate = copy_df.Date.astype('str')
        for i in range(len(xdate)):
            xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

        self.axes[0].plot(xdate, copy_df['close'], linewidth=0.7, color='k')
        candlestick2_ohlc(self.axes[0], copy_df['open'], copy_df['high'], copy_df['low'], copy_df['close'],
                                width=0.5, colorup='r', colordown='b')

        self.fig.suptitle("stock chart")
        self.fig.autofmt_xdate(rotation=45)
        self.axes[0].set_xlabel("Date")
        self.axes[0].set_ylabel("Price")
        self.axes[0].xaxis.set_major_locator(ticker.MaxNLocator(25))
        self.axes[0].legend(loc='best')  # legend 위치
        self.axes[0].grid()

        scale = 1.1
        self.zoom_factory(self.axes[0], base_scale=scale)
        self.pan_factory(self.axes[0])

        self.draw()