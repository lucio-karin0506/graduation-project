import PySide2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import os
import sys

from p407_gui.interface import directory_tree, graph_canvas
from p407_gui.module.handling_file import get_refined_path

'''
기본 백테스트 화면
1. 주문 폴더
2. 백테스트 기본 값 입력
3. 수익률 그래프 창
'''
class basic_backtest(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '기본백테스트'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('기본백테스트')

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수평 정렬
        vlay = QVBoxLayout(widget)

        # 주문 생성 에디터 위젯 가져오기
        basic_backtest = basic_backtest_editor(self)
        vlay1 = QVBoxLayout()
        vlay1.addWidget(basic_backtest)
        vlay.addLayout(vlay1)


class basic_backtest_editor(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        #전체 레이아웃
        layout = QHBoxLayout()

        # Left Layout(directory tree, 주문파일 & 초기자본금 입력, 실행버튼)
        leftLayout = QHBoxLayout()

        # 종목 폴더
        vlay1 = QVBoxLayout()
        self.dir_label = QLabel('주문폴더')
        self.dir_tree = directory_tree.DirectoryTreeView()

        vlay1.addWidget(self.dir_label)
        vlay1.addWidget(self.dir_tree)

        # (주문파일, 파일입력, 초기자본금, 실행버튼, 손익률 통계자료표)
        vlay2 = QVBoxLayout()

        # 주문파일, 초기자본금 입력, 파일 입력 버튼, 실행버튼
        hlay1 = QHBoxLayout()
        hlay2 = QHBoxLayout()

        # 주문파일
        self.order_file = QLabel('주문파일')
        self.order_file_edit = QLineEdit()
        hlay1.addWidget(self.order_file)
        hlay1.addWidget(self.order_file_edit)

        # 파일입력 버튼
        self.order_file_button = QPushButton('파일입력')

        # 초기자본금
        self.init_money = QLabel('운용 금액')
        self.init_money_edit = QLineEdit()
        hlay2.addWidget(self.init_money)
        hlay2.addWidget(self.init_money_edit)

        # 실행버튼
        self.basic_button = QPushButton('백테스트 실행')

        # 손익률 통계자료표 위젯
        self.static_table_label = QLabel('통계자료표')

        self.static_table = QTableWidget()
        self.static_table.resize(300, 200)
        # 표의 크기를 지정
        self.static_table.setColumnCount(2)
        self.static_table.setRowCount(5)
        # 열 제목 지정
        self.static_table.setHorizontalHeaderLabels(['이름', '값'])
        # 통계자료표 내용
        self.static_table.setItem(0, 0, QTableWidgetItem('매수횟수'))
        self.static_table.setItem(1, 0, QTableWidgetItem('매도횟수'))
        self.static_table.setItem(2, 0, QTableWidgetItem('최저손익률'))
        self.static_table.setItem(3, 0, QTableWidgetItem('최고손익률'))
        self.static_table.setItem(4, 0, QTableWidgetItem('최종손익률'))
        self.static_table.setItem(0, 1, QTableWidgetItem('3'))
        self.static_table.setItem(1, 1, QTableWidgetItem('3'))
        self.static_table.setItem(2, 1, QTableWidgetItem('3'))
        self.static_table.setItem(3, 1, QTableWidgetItem('3'))
        self.static_table.setItem(4, 1, QTableWidgetItem('3'))
        self.static_table.setItem(5, 1, QTableWidgetItem('3'))

        vlay2.addLayout(hlay1)
        vlay2.addWidget(self.order_file_button)
        vlay2.addLayout(hlay2)
        vlay2.addWidget(self.basic_button)
        vlay2.addWidget(self.static_table_label)
        vlay2.addWidget(self.static_table)

        leftLayout.addLayout(vlay1)
        leftLayout.addLayout(vlay2)

        # 수익률 그래프 위젯
        rightLayout = QVBoxLayout()
        # 그래프 캔버스 레이아웃 선언
        self.setAcceptDrops(True)
        self.canvas = graph_canvas.PlotCanvas(self, width=10, height=8)
        self.toolbar = graph_canvas.NavigationToolbar(self.canvas, self)
        rightLayout.addWidget(self.toolbar)
        rightLayout.addWidget(self.canvas)

        # 그래프 종류 선택 위젯 레이아웃
        comboLayout = QVBoxLayout()
        self.cb_option = QComboBox(self)
        self.cb_option.addItem('월별 수익률', 'month_profit')
        self.cb_option.addItem('누적 수익률', 'acc_profit')

        # 자산 흐름도 표 다이얼로그 띄우는 버튼
        self.capital = QPushButton('자산 흐름표')

        comboLayout.addWidget(self.cb_option)
        comboLayout.addWidget(self.capital)
        comboLayout.addStretch(1)

        # 전체 레이아웃 병합 및 조정
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.addLayout(comboLayout)
        layout.setStretchFactor(leftLayout, 0)
        layout.setStretchFactor(rightLayout, 1)
        self.setLayout(layout)

    def dropEvent(self, event: QDropEvent):
        print("Drop!")
        path = get_refined_path(event.mimeData().text())
        print(get_refined_path(event.mimeData().text()))
        # self.canvas._plot_money_flow(path)
        self.path = path
        if self.cb_option.currentData() == 'moneyflow':
            self.canvas._plot_money_flow(path)
        elif self.cb_option.currentData() == 'per':
            self.canvas._plot_per(path)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = basic_backtest()
    mainWin.show()
    sys.exit(app.exec_())