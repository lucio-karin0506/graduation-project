from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.Qt import Qt, QFileSystemModel
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

import os
import sys
import copy
import platform
import pandas as pd

import p407_gui.gathering
import p407_gui.tech_indi

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import style

from mplfinance.original_flavor import candlestick2_ochl


if platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
elif platform.system() == 'Linux':
    font_name = font_manager.FontProperties(fname="/src/doozy.git/setup/font/GSTTF.ttf").get_name()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '매매 대상 설정'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('Ready')

        # 메뉴바
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&파일')
        getDataMenu = menubar.addMenu('&매매 대상 설정')
        strategyMenu = menubar.addMenu('&전략 생성')
        backtestMenu = menubar.addMenu('&백테스팅')
        portfolioMenu = menubar.addMenu('&수익 포트폴리오')
        exitMenu = menubar.addMenu('&종료')

        get_file = QAction('&파일 불러오기', self)
        store_file = QAction('&파일 저장하기', self)
        fileMenu.addAction(get_file)
        fileMenu.addAction(store_file)

        basic_backtest = QAction('&기본 백테스팅', self)
        labeler_backtest = QAction('&레이블러 백테스팅', self)
        backtestMenu.addAction(basic_backtest)
        backtestMenu.addAction(labeler_backtest)

        # 메뉴바 종료 버튼 이벤트 처리
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        exitMenu.addAction(exitButton)

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수직 정렬
        vlay = QVBoxLayout(widget)

        # 그래프 위젯 가져오기
        m = VisualizationWidget(self)
        vlay.addWidget(m)


#그래프 시각화하여 보여주는 클래스
class VisualizationWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.setAcceptDrops(True)
        self.canvas = PlotCanvas(self, width=10, height=8)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.initUI()
        self.setGeometry(100, 100, 800, 800)

    def initUI(self):
        hlay = QHBoxLayout()

        # 주식 정보 기입하는 기본 버튼 위젯 생성
        global line1, line2, line3, line4

        codeLabel = QLabel('주식 코드:', self)
        line1 = QLineEdit(self)
        hlay.addWidget(codeLabel)
        hlay.addWidget(line1)
        hlay.addItem(QSpacerItem(100, 10, QSizePolicy.Expanding))

        startDateLabel = QLabel('시작 날짜:', self)
        line2 = QLineEdit(self)
        hlay.addWidget(startDateLabel)
        hlay.addWidget(line2)
        hlay.addItem(QSpacerItem(100, 10, QSizePolicy.Expanding))

        endDateLabel = QLabel('끝 날짜:', self)
        line3 = QLineEdit(self)
        hlay.addWidget(endDateLabel)
        hlay.addWidget(line3)
        hlay.addItem(QSpacerItem(100, 10, QSizePolicy.Expanding))

        dtypeLabel = QLabel('봉 타입:', self)
        line4 = QLineEdit(self)
        hlay.addWidget(dtypeLabel)
        hlay.addWidget(line4)
        hlay.addItem(QSpacerItem(100, 10, QSizePolicy.Expanding))

        # figure 생성 및 figure-canvas 연동(그래프)
        fig = plt.Figure()
        canvas = FigureCanvas(fig)

        # 왼쪽 그래프 배치(툴바, 그래프 캔버스)
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.toolbar)
        leftLayout.addWidget(self.canvas)

        # 데이터 저장 버튼
        storeButton = QPushButton("데이터 저장")
        storeButton.clicked.connect(self.store_data)

        #기술적지표 그룹박스 레이아웃 생성
        groupbox = QGroupBox('기술적 지표')

        global moveLine_check, labeling_check, rsi_check, macd_check, bb_check, fast_stoch_check, slow_stoch_check

        moveLine_check = QCheckBox('이동평균선')
        labeling_check = QCheckBox('레이블링')
        rsi_check = QCheckBox('RSI')
        macd_check = QCheckBox('MACD')
        bb_check = QCheckBox('Bolinger Band')
        fast_stoch_check = QCheckBox('Fast Stochastic')
        slow_stoch_check = QCheckBox('Slow Stochastic')

        #기술적 지표 그룹 박스 수직 정렬
        vbox = QVBoxLayout()
        vbox.addWidget(moveLine_check)
        vbox.addWidget(labeling_check)
        vbox.addWidget(rsi_check)
        vbox.addWidget(macd_check)
        vbox.addWidget(bb_check)
        vbox.addWidget(fast_stoch_check)
        vbox.addWidget(slow_stoch_check)
        groupbox.setLayout(vbox)
        groupbox.setMaximumSize(200, 300)

        #각각 체크박스 선택 시 이벤트 발생 처리 함수 연결
        moveLine_check.stateChanged.connect(self.tech_value_check)
        labeling_check.stateChanged.connect(self.tech_value_check)
        rsi_check.stateChanged.connect(self.tech_value_check)
        macd_check.stateChanged.connect(self.tech_value_check)
        bb_check.stateChanged.connect(self.tech_value_check)
        fast_stoch_check.stateChanged.connect(self.tech_value_check)
        slow_stoch_check.stateChanged.connect(self.tech_value_check)

        #그래프 생성 버튼 위젯
        graphButton = QPushButton("DRAW Graph")
        graphButton.clicked.connect(self.get_info_graph)

        #오른쪽 기술적지표 및 그래프 생성 버튼 배치
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(storeButton)
        rightLayout.addWidget(groupbox)
        rightLayout.addWidget(graphButton)

        #그래프 레이아웃 배치 조정
        vlay = QVBoxLayout()
        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)
        vlay.addLayout(hlay)
        vlay.addLayout(layout)

        self.setLayout(vlay)

    '''
    1. 주식 그래프 기본 파라미터 정보 처리 & 각 지표 값 그래프 체크박스 기능 연결
    2. 주가 데이터 csv파일 root 디렉토리 저장
    '''
    def get_info_graph(self):
        global df1, stock_code, start_date, end_date, dtype
        stock_code = line1.text()
        start_date = line2.text()
        end_date = line3.text()
        dtype = line4.text()

        mod = stock_system_gui.gathering.Gathering()
        df1 = mod.get_stock(stock_code, start_date, end_date, dtype)

        self.canvas.draw_graph(df1, 'off')

    #주가 데이터 csv파일 저장
    def store_data(self):
        import csv
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fname = QFileDialog.getSaveFileName(self, '파일 저장', '',
                                            'All File(*);; CSV File(*.csv)', options=options)

        if fname[0]:
            df1.to_csv(r'C:\Temp')
        else:
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')


    def tech_value_check(self):
        if moveLine_check.isChecked():
            print('yes')
        if labeling_check.isChecked():
            print('yes')
        if rsi_check.isChecked():
            print('yes')
        if macd_check.isChecked():
            print('yes')
        if bb_check.isChecked() == True:
            self.canvas.draw_graph(df1, 'bb')
        if fast_stoch_check.isChecked():
            print('yes')
        if slow_stoch_check.isChecked():
            print('yes')


#그래프 캔버스 디자인 클래스 & 지표 값 종류에 따른 그래프 구현 이벤트 처리
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


    #Draw graph 버튼 누를 때 그래프 차트 그리는 함수
    def draw_graph(self, df, status):
        copy_df = copy.deepcopy(df)
        copy_df.reset_index(inplace=True)

        # 한글 폰트 지정
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)

        # x-축 날짜
        xdate = copy_df.Date.astype('str')
        for i in range(len(xdate)):
            xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

        if status == 'off':
            self.axes[0].plot(xdate, copy_df['close'], linewidth=0.7, color='k')
            candlestick2_ochl(self.axes[0], copy_df['open'], copy_df['high'], copy_df['low'], copy_df['close'], width=0.5,
                                colorup='r', colordown='b')

        elif status == 'bb':
            self.axes[0].plot(xdate, copy_df['ubb'], label="Upper limit", linewidth=0.7, color='k')
            self.axes[0].plot(xdate, copy_df['mbb'], label="center line", linewidth=0.7, color='y')
            self.axes[0].plot(xdate, copy_df['lbb'], label="Lower limit", linewidth=0.7, color='k')

            candlestick2_ochl(self.axes[0], copy_df['open'], copy_df['high'], copy_df['low'], copy_df['close'],
                          width=0.5, colorup='r', colordown='b')

        self.fig.suptitle("stock chart")
        self.axes[0].set_xlabel("Date")
        self.axes[0].set_ylabel("Price")
        self.axes[0].xaxis.set_major_locator(ticker.MaxNLocator(25))
        self.axes[0].legend(loc='best') # legend 위치
        self.axes[0].grid()

        scale = 1.1
        figZoom = self.zoom_factory(self.axes[0], base_scale=scale)
        figPan = self.pan_factory(self.axes[0])

        self.draw()


    def update_subplot(self, count):
        [self.fig.delaxes(ax) for ax in self.axes]
        self.axes = [self.fig.add_subplot(count, 1, i + 1) for i in range(count)]
        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())