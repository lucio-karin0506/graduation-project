import platform
import PySide2
import sys
import os
import copy
import pandas as pd

from PySide2.QtGui import *
from PySide2.QtWidgets import *

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import style

from p407_gui.chart_visualization.basic_drawing import basic_drawing

from mplfinance.original_flavor import candlestick2_ohlc

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = [self.fig.add_subplot(111)]

        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.plot()

    def zoom_factory(self, ax, base_scale=2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata  # get event x location
            ydata = event.ydata  # get event y location

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        # return the function
        return onMotion

    # csv 파일 drag 하여 일봉 기본 차트 띄우는 함수
    def basic_d_graph(self, path):
        basic_drawing.basic_d_graph(self, path)

    # csv 파일 drag 하여 주봉 기본 차트 띄우는 함수
    def basic_w_graph(self, path):
        basic_drawing.basic_w_graph(self, path)

    # 기술적 지표 차트 띄우는 함수
    def draw_tech_indi(self, df, period, state):
        copy_df = copy.deepcopy(df)
        copy_df.reset_index(inplace=True)
        # indicator.add_MA(copy_df, period, price)

        # 한글 폰트 지정
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
        fig, ax = plt.subplots(figsize=(12, 10))

        # x-축 날짜
        xdate = copy_df.Date.astype('str')
        for i in range(len(xdate)):
            xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

        # 이동평균선 차트
        if state == 'ma':
            self.axes[0].plot(xdate, copy_df['ma_' + str(period)], 'g-', label='MA' + str(period))

        # 기본차트
        # ax.plot(xdate, copy_df[price], 'k-')
        candlestick2_ohlc(self.axes[0], copy_df['open'], copy_df['high'],
                          copy_df['low'], copy_df['close'], width=0.6, colorup='r', colordown='b')

        # self.fig.set_title('Stock Chart', fontsize=20)
        self.fig.autofmt_xdate(rotation=45)
        self.axes[0].set_xlabel("Date")
        self.axes[0].set_ylabel("Price")
        self.axes[0].xaxis.set_major_locator(ticker.MaxNLocator(25))
        self.axes[0].legend(loc='best')  # legend 위치
        self.axes[0].grid()

        self.draw()

        print('test1111')

    def update_subplot(self, count):
        [self.fig.delaxes(ax) for ax in self.axes]
        self.axes = [self.fig.add_subplot(count, 1, i + 1) for i in range(count)]
        self.draw()