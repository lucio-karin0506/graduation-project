import platform
import PySide2
import sys
import os
import copy
import pandas as pd

from PySide2.QtGui import *
from PySide2.QtWidgets import *

from p407_gui.module.handling_file import get_refined_path
from p407_gui.interface import stock_add_dialog, directory_tree, graph_canvas, indicator_tree

from p407_gui.interface.tech_indi_param_dialog import (ma_dialog, ema_dialog, cmo_dialog,
                                                rsi_dialog, bb_dialog, macd_dialog, stoch_fast_dialog,
                                                stoch_slow_dialog)

from p407_gui.interface.label_indi_param_dialog import (bbands_label_dialog, candle_shape_dialog, candle_type_dialog,
                                                dema_cross_dialog, macd_cross_dialog, macd_label_dialog, n_gap_dialog,
                                                roc_dialog, sma_cross_dialog, stoch_label_dialog, stochf_label_dialog,
                                                three_blue_dialog, three_red_dialog, vwma_cross_dialog)

'''
종목 차트 화면
'''
class stock_chart(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '종목차트'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('종목차트')

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수평 정렬
        hlay = QHBoxLayout(widget)

        # 그래프 및 전체 위젯 가져오기
        m = stock_chart_editor(self)
        hlay.addWidget(m)


class stock_chart_editor(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.path = ''

        # Left Layout (종목 다운로드 버튼, 종목 폴더, 지표 리스트)
        leftLayout = QVBoxLayout()

        # 종목 다운로드 버튼
        self.stock_button = QPushButton('종목다운로드')
        self.stock_button.clicked.connect(self.get_stock_dialog)

        # 종목폴더 디렉토리
        self.dir_label = QLabel('종목폴더')
        self.dir_tree = directory_tree.DirectoryTreeView()
        self.stock_select_button = QPushButton('선택')

        # 지표 리스트 위젯
        self.indi_label = QLabel('지표')
        self.indi_tree = indicator_tree.IndicatorTreeView()
        self.indi_tree.setAlternatingRowColors(True)
        self.indi_tree.header().setVisible(False)

        leftLayout.addWidget(self.stock_button)
        leftLayout.addWidget(self.dir_label)
        leftLayout.addWidget(self.dir_tree)
        leftLayout.addWidget(self.stock_select_button)
        leftLayout.addWidget(self.indi_label)
        leftLayout.addWidget(self.indi_tree)

        # Center Layout (차트 캔버스)
        centerLayout = QVBoxLayout()

        self.setAcceptDrops(True)
        self.canvas = graph_canvas.PlotCanvas(self, width=10, height=8)
        self.toolbar = graph_canvas.NavigationToolbar(self.canvas, self)

        centerLayout.addWidget(self.toolbar)
        centerLayout.addWidget(self.canvas)

        # Right Layout (봉 타입 콤보박스, 지표 & 레이블 리스트 위젯, 지표 추가 버튼)
        rightLayout = QVBoxLayout()

        self.cb_option = QComboBox(self)
        self.cb_option.addItem('일봉', 'd')
        self.cb_option.addItem('주봉', 'w')
        self.cb_option.currentTextChanged.connect(self.change_subplot)

        # 기술적 지표 리스트 박스
        self.tech_list_label = QLabel('기술적 지표')
        self.tech_list = QListWidget()
        self.tech_list.addItems(['이동평균', 'RSI', 'MACD', 'BollingerBand', 'Stochastic Fast', 'Stochastic Slow',
                                 'EMA', 'CMO'])

        self.tech_list_button = QPushButton('추가')
        self.tech_list_button.clicked.connect(self.get_tech_indi_param_dialog)

        # 레이블 지표 리스트 박스
        self.label_list_label = QLabel('레이블 지표')
        self.label_list = QListWidget()
        self.label_list.addItems(['캔들 종류', '캔들 모양', '적삼병', '흑삼병', '갭 상승/하락', '가격 변화 비율', '단순이동평균',
                                  '이중지수이동평균', '거래량가중이동평균', 'MACD', 'BollingerBand', 'MACD Cross',
                                  'Stochastic Fast Cross', 'Stochastic Slow Cross'])

        self.label_list_button = QPushButton('추가')
        self.label_list_button.clicked.connect(self.get_label_indi_param_dialog)

        rightLayout.addWidget(self.cb_option)
        rightLayout.addWidget(self.tech_list_label)
        rightLayout.addWidget(self.tech_list)
        rightLayout.addWidget(self.tech_list_button)
        rightLayout.addStretch(2)
        rightLayout.addWidget(self.label_list_label)
        rightLayout.addWidget(self.label_list)
        rightLayout.addWidget(self.label_list_button)

        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(centerLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(centerLayout, 0)
        layout.setStretchFactor(rightLayout, 1)

        self.setLayout(layout)

    def change_subplot(self):
        if self.cb_option.currentData() == 'd':
            self.canvas.update_subplot(1)
        elif self.cb_option.currentData() == 'w':
            self.canvas.update_subplot(1)

    '''
    파일 경로 디렉토리에서 그래프 캔버스로 drag&drop 할 시 발생하는 이벤트 처리
    1. 기본 주가 차트 생성
    2. 지표 리스트 박스에 종목 이름, 기술적지표&레이블지표 텍스트, 기존 파일에 지표 있을 시 하부 아이템에 등록
    '''
    def dropEvent(self, event: QDropEvent):
        print("Drop!")
        path = get_refined_path(event.mimeData().text())
        print(get_refined_path(event.mimeData().text()))
        self.path = path
        # 일봉 콤보 아이템 선택 시 일봉 차트
        if self.cb_option.currentData() == 'd':
            self.canvas.basic_d_graph(path)
        # 주봉 콤보 아이템 선택 시 주봉 차트
        elif self.cb_option.currentData() == 'w':
            self.canvas.basic_w_graph(path)

        # 지표 리스트 박스에 파일 경로 정보 전달
        self.indi_tree.get_path(self.path)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    # 종목 추가 버튼 클릭 시 종목 추가 다이얼로그 이동
    def get_stock_dialog(self):
        dialog = stock_add_dialog.stock_add()
        dialog.showModal()

    # 기술적 지표 리스트 박스에서 지표 클릭 시 다이얼로그 이동
    def get_tech_indi_param_dialog(self):
        row = self.tech_list.currentRow()
        item = self.tech_list.item(row)

        if item.text() == '이동평균':
            dialog = ma_dialog.ma_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.ma_period = 'ma_' + dialog.period_edit.text()
            self.ma = QTreeWidgetItem([self.ma_period])
            self.indi_tree.item_ma.addChild(self.ma)

        elif item.text() == 'RSI':
            dialog = rsi_dialog.rsi_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.rsi_period = 'rsi_' + dialog.period_edit.text()
            self.rsi = QTreeWidgetItem([self.rsi_period])
            self.indi_tree.item_rsi.addChild(self.rsi)

        elif item.text() == 'MACD':
            dialog = macd_dialog.macd_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.fast_period = dialog.fast_edit.text()
            self.slow_period = dialog.slow_edit.text()
            self.signal_period = dialog.signal_edit.text()

            self.macd_origin = 'macd_' + self.fast_period + '_' + self.slow_period + '_' + self.signal_period
            self.macd_signal = 'macd_signal_' + self.fast_period + '_' + self.slow_period + '_' + self.signal_period
            self.macd_hist = 'macd_hist_' + self.fast_period + '_' + self.slow_period + '_' + self.signal_period

            self.macd_origin_item = QTreeWidgetItem([self.macd_origin])
            self.macd_signal_item = QTreeWidgetItem([self.macd_signal])
            self.macd_hist_item = QTreeWidgetItem([self.macd_hist])

            self.indi_tree.item_macd.addChild(self.macd_origin_item)
            self.indi_tree.item_macd.addChild(self.macd_signal_item)
            self.indi_tree.item_macd.addChild(self.macd_hist_item)

        elif item.text() == 'BollingerBand':
            dialog = bb_dialog.bb_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.bb_period = dialog.period_edit.text()
            self.nbdevup = dialog.up_edit.text()
            self.nbdevdn = dialog.down_edit.text()

            self.bb_ubb = 'ubb_' + self.bb_period + '_' + self.nbdevup + '_' + self.nbdevdn
            self.bb_mbb = 'mbb_' + self.bb_period + '_' + self.nbdevup + '_' + self.nbdevdn
            self.bb_lbb = 'lbb_' + self.bb_period + '_' + self.nbdevup + '_' + self.nbdevdn

            self.bb_ubb_item = QTreeWidgetItem([self.bb_ubb])
            self.bb_mbb_item = QTreeWidgetItem([self.bb_mbb])
            self.bb_lbb_item = QTreeWidgetItem([self.bb_lbb])

            self.indi_tree.item_bb.addChild(self.bb_ubb_item)
            self.indi_tree.item_bb.addChild(self.bb_mbb_item)
            self.indi_tree.item_bb.addChild(self.bb_lbb_item)

        elif item.text() == 'Stochastic Fast':
            dialog = stoch_fast_dialog.stoch_fast_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.fastk = dialog.fastk_edit.text()
            self.fastd = dialog.fastd_edit.text()

            self.stochf_fastk = 'fastk_' + self.fastk + '_' + self.fastd
            self.stochf_fastd = 'fastk_' + self.fastk + '_' + self.fastd

            self.stochf_fastk_item = QTreeWidgetItem([self.stochf_fastk])
            self.stochf_fastd_item = QTreeWidgetItem([self.stochf_fastd])

            self.indi_tree.item_stochf.addChild(self.stochf_fastk_item)
            self.indi_tree.item_stochf.addChild(self.stochf_fastd_item)

        elif item.text() == 'Stochastic Slow':
            dialog = stoch_slow_dialog.stoch_slow_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.stoch_fastk = dialog.fastk_edit.text()
            self.slowk = dialog.slowk_edit.text()
            self.slowd = dialog.slowd_edit.text()

            self.stoch_slowk = 'slowk_' + self.stoch_fastk + '_' + self.slowk + '_' + self.slowd
            self.stoch_slowd = 'slowd_' + self.stoch_fastk + '_' + self.slowk + '_' + self.slowd

            self.stoch_slowk_item = QTreeWidgetItem([self.stoch_slowk])
            self.stoch_slowd_item = QTreeWidgetItem([self.stoch_slowd])

            self.indi_tree.item_stochs.addChild(self.stoch_slowk_item)
            self.indi_tree.item_stochs.addChild(self.stoch_slowd_item)

        elif item.text() == 'EMA':
            dialog = ema_dialog.ema_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.ema_period = 'ema_' + dialog.period_edit.text()
            self.ema = QTreeWidgetItem([self.ema_period])
            self.indi_tree.item_ema.addChild(self.ema)

        elif item.text() == 'CMO':
            dialog = cmo_dialog.cmo_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 지표 목록 추가
            self.cmo_period = 'cmo_' + dialog.period_edit.text()
            self.cmo = QTreeWidgetItem([self.cmo_period])
            self.indi_tree.item_cmo.addChild(self.cmo)

    # 레이블 지표 리스트 박스에서 지표 클릭 시 다이얼로그 이동
    def get_label_indi_param_dialog(self):
        row = self.label_list.currentRow()
        item = self.label_list.item(row)
        if item.text() == '캔들 종류':
            candle_type_dialog.confirmIt(self.path)
            QMessageBox.information(self, "메시지", "파라미터 설정이 완료되었습니다!", QMessageBox.Yes)

        elif item.text() == '캔들 모양':
            candle_shape_dialog.confirmIt(self.path)
            QMessageBox.information(self, "메시지", "파라미터 설정이 완료되었습니다!", QMessageBox.Yes)

        elif item.text() == '적삼병':
            dialog1 = three_red_dialog.three_red_Param(item.text(), self.path, self)
            dialog1.showModal()

            # 지표 리스트 추가
            self.three_red_item = QTreeWidgetItem(['three_red'])
            self.indi_tree.item_3red.addChild(self.three_red_item)

        elif item.text() == '흑삼병':
            dialog1 = three_blue_dialog.three_blue_Param(item.text(), self.path, self)
            dialog1.showModal()

            # 지표 리스트 추가
            self.three_blue_item = QTreeWidgetItem(['three_blue'])
            self.indi_tree.item_3blue.addChild(self.three_blue_item)

        elif item.text() == '갭 상승/하락':
            dialog = n_gap_dialog.ngap_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.ngap_colName = dialog.num_edit.text()
            self.ngap_num_item = QTreeWidgetItem(['gap_' + self.ngap_colName])
            self.indi_tree.item_ngap.addChild(self.ngap_num_item)

        elif item.text() == '가격 변화 비율':
            dialog = roc_dialog.roc_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.roc_prevDay = int(dialog.period_edit.text())
            self.roc_target = str(dialog.target_option.currentData())

            self.roc_colName = f'roc_{self.roc_prevDay}({self.roc_target})'

            self.roc_param_item = QTreeWidgetItem([self.roc_colName])
            self.indi_tree.item_roc.addChild(self.roc_param_item)

        elif item.text() == '단순이동평균':
            dialog = sma_cross_dialog.sma_cross_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.sma_short = int(dialog.short_period_edit.text())
            self.sma_long = int(dialog.long_period_edit.text())
            self.sma_target = str(dialog.target_option.currentData())

            self.sma_colName = f'ma_cross_{self.sma_short}_{self.sma_long}({self.sma_target})'

            self.sma_param_item = QTreeWidgetItem([self.sma_colName])
            self.indi_tree.item_sma_cross.addChild(self.sma_param_item)

        elif item.text() == '이중지수이동평균':
            dialog = dema_cross_dialog.dema_cross_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.dema_short = int(dialog.short_period_edit.text())
            self.dema_long = int(dialog.long_period_edit.text())
            self.dema_target = str(dialog.target_option.currentData())

            self.dema_colName = f'dema_cross_{self.dema_short}_{self.dema_long}({self.dema_target})'

            self.dema_param_item = QTreeWidgetItem([self.dema_colName])
            self.indi_tree.item_dema_cross.addChild(self.dema_param_item)

        elif item.text() == '거래량가중이동평균':
            dialog = vwma_cross_dialog.vwma_cross_label_param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.vwma_short = int(dialog.short_period_edit.text())
            self.vwma_long = int(dialog.long_period_edit.text())
            self.vwma_target = str(dialog.target_option.currentData())

            self.vwma_colName = f'vwma_cross_{self.vwma_short}_{self.vwma_long}({self.vwma_target})'

            self.vwma_param_item = QTreeWidgetItem([self.vwma_colName])
            self.indi_tree.item_vwma_cross.addChild(self.vwma_param_item)

        elif item.text() == 'MACD':
            dialog = macd_label_dialog.macd_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.macdlb_short = int(dialog.short_period_edit.text())
            self.macdlb_long = int(dialog.long_period_edit.text())
            self.macdlb_target = str(dialog.target_option.currentData())

            self.macdlb_colName = f'macd_{self.macdlb_short}_{self.macdlb_long}({self.macdlb_target})'

            self.macdlb_param_item = QTreeWidgetItem([self.macdlb_colName])
            self.indi_tree.item_macd_label.addChild(self.macdlb_param_item)

        elif item.text() == 'BollingerBand':
            dialog = bbands_label_dialog.bbands_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.bblb_period = int(dialog.period_edit.text())
            self.bblb_multid = int(dialog.multid_edit.text())
            self.bblb_target = str(dialog.target_option.currentData())

            self.bblb_colName = f'bb_{self.bblb_period}_{self.bblb_multid}({self.bblb_target})'

            self.bblb_param_item = QTreeWidgetItem([self.bblb_colName])
            self.indi_tree.item_bb_label.addChild(self.bblb_param_item)

        elif item.text() == 'MACD Cross':
            dialog = macd_cross_dialog.macd_cross_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.macdCross_short = int(dialog.short_period_edit.text())
            self.macdCross_long = int(dialog.long_period_edit.text())
            self.macdCross_signal = int(dialog.signal_period_edit.text())
            self.macdCross_target = str(dialog.target_option.currentData())

            self.macdCross_colName = f'macd_cross_{self.macdCross_short}_' \
                                     f'{self.macdCross_long}_{self.macdCross_signal}({self.macdCross_target})'

            self.macdCross_param_item = QTreeWidgetItem([self.macdCross_colName])
            self.indi_tree.item_macd_cross.addChild(self.macdCross_param_item)

        elif item.text() == 'Stochastic Fast Cross':
            dialog = stochf_label_dialog.stoch_fast_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.stochflb_fastk = int(dialog.fastk_period_edit.text())
            self.stochflb_fastd = int(dialog.fastd_period_edit.text())

            self.stochflb_colName = f'stochf_{self.stochflb_fastk}_{self.stochflb_fastd}'

            self.stochflb_param_item = QTreeWidgetItem([self.stochflb_colName])
            self.indi_tree.item_stochf_label.addChild(self.stochflb_param_item)

        elif item.text() == 'Stochastic Slow Cross':
            dialog = stoch_label_dialog.stochastic_slow_label_Param(item.text(), self.path, self)
            dialog.showModal()

            # 지표 리스트 추가
            self.stochlb_fastk = int(dialog.fastk_period_edit.text())
            self.stochlb_slowk = int(dialog.slowk_period_edit.text())
            self.stochlb_slowd = int(dialog.slowd_period_edit.text())

            self.stochlb_colName = f'stoch_{self.stochlb_fastk}_{self.stochlb_slowk}_{self.stochlb_slowd}'

            self.stochlb_param_item = QTreeWidgetItem([self.stochlb_colName])
            self.indi_tree.item_stochs_label.addChild(self.stochlb_param_item)


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = stock_chart()
    mainWin.show()
    sys.exit(app.exec_())