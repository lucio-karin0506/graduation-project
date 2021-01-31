import PySide2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import os
import sys

from p407_gui.interface import directory_tree, graph_canvas, hit_ratio_dialog
from p407_gui.module.handling_file import get_refined_path

'''
레이블 백테스트 화면
1. 주문 생성 에디터
2. 디버그 로깅 창
'''
class label_backtest(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '레이블백테스트'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('레이블백테스트')

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수평 정렬
        vlay = QVBoxLayout(widget)

        # 주문 생성 에디터 위젯 가져오기
        label_backtest = label_backtest_editor(self)
        vlay1 = QVBoxLayout()
        vlay1.addWidget(label_backtest)
        vlay.addLayout(vlay1)


class label_backtest_editor(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        #전체 레이아웃
        layout = QHBoxLayout()

        # Left Layout(vlay1 + vlay2)
        leftLayout = QHBoxLayout()

        # 종목 폴더
        vlay1 = QVBoxLayout()
        self.dir_label = QLabel('주문폴더')
        self.dir_tree = directory_tree.DirectoryTreeView()

        vlay1.addWidget(self.dir_label)
        vlay1.addWidget(self.dir_tree)

        # 주문폴더, 파일입력버튼, 레이블파라미터 그룹박스, 레이블 그래프 생성버튼
        # 기본 백테스팅 파일, 버튼, 레이블 백테스팅 파일, 버튼, 레이블 백테스팅 실행 버튼
        vlay2 = QVBoxLayout()

        # 주문폴더 입력, 실행버튼
        hlay1 = QHBoxLayout()
        # 기본 백테스팅 파일 입력, 실행버튼
        hlay2 = QHBoxLayout()
        # 레이블 백테스팅 파일 입력, 실행버튼
        hlay3 = QHBoxLayout()

        # 주문폴더
        self.stock_file = QLabel('주문파일')
        self.stock_file_edit = QLineEdit()
        hlay1.addWidget(self.stock_file)
        hlay1.addWidget(self.stock_file_edit)

        # 파일입력 버튼
        self.stock_file_button = QPushButton('파일입력')

        # 레이블 파라미터 그룹박스
        self.label_box = QGroupBox('레이블 파라미터')
        box_lay = QVBoxLayout()
        param_input_lay1 = QHBoxLayout()
        param_input_lay2 = QHBoxLayout()
        param_input_lay3 = QHBoxLayout()
        param_input_lay4 = QHBoxLayout()

        self.param1_label = QLabel('RRPB')
        self.param1_edit = QLineEdit()
        param_input_lay1.addWidget(self.param1_label)
        param_input_lay1.addWidget(self.param1_edit)

        self.param2_label = QLabel('RFPT')
        self.param2_edit = QLineEdit()
        param_input_lay2.addWidget(self.param2_label)
        param_input_lay2.addWidget(self.param2_edit)

        self.param3_label = QLabel('PBR')
        self.param3_edit = QLineEdit()
        param_input_lay3.addWidget(self.param3_label)
        param_input_lay3.addWidget(self.param3_edit)

        self.param4_label = QLabel('BBR')
        self.param4_edit = QLineEdit()
        param_input_lay4.addWidget(self.param4_label)
        param_input_lay4.addWidget(self.param4_edit)

        box_lay.addLayout(param_input_lay1)
        box_lay.addLayout(param_input_lay2)
        box_lay.addLayout(param_input_lay3)
        box_lay.addLayout(param_input_lay4)
        self.label_box.setLayout(box_lay)

        # 레이블 그래프 생성 버튼
        self.label_graph_button = QPushButton('레이블 그래프 생성')

        # 기본 백테스팅 파일
        self.basic_file = QLabel('기본 백테스팅 파일')
        self.basic_file_edit = QLineEdit()
        hlay2.addWidget(self.basic_file)
        hlay2.addWidget(self.basic_file_edit)

        # 입력버튼
        self.basic_input_button = QPushButton('파일입력')

        # 레이블 백테스팅 파일
        self.label_file = QLabel('레이블 백테스팅 파일')
        self.label_file_edit = QLineEdit()
        hlay3.addWidget(self.label_file)
        hlay3.addWidget(self.label_file_edit)

        # 입력버튼
        self.label_input_button = QPushButton('파일입력')

        # 입력버튼
        self.label_exec = QPushButton('레이블 백테스팅 실행')
        self.label_exec.clicked.connect(self.get_hitRatio_dialog)

        vlay2.addLayout(hlay1)
        vlay2.addWidget(self.stock_file_button)
        vlay2.addWidget(self.label_box)
        vlay2.addWidget(self.label_graph_button)
        vlay2.addLayout(hlay2)
        vlay2.addWidget(self.basic_input_button)
        vlay2.addLayout(hlay3)
        vlay2.addWidget(self.label_input_button)
        vlay2.addWidget(self.label_exec)

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

        # 전체 레이아웃 병합 및 조정
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
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

    def get_hitRatio_dialog(self):
        dialog = hit_ratio_dialog.hit_ratio()
        dialog.showModal()


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = label_backtest()
    mainWin.show()
    sys.exit(app.exec_())