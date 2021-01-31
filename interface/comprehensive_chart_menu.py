import PySide2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import os
import sys

from p407_gui.interface import directory_tree, graph_canvas
from p407_gui.module.handling_file import get_refined_path

'''
종합 차트 화면 (내부 및 외부 데이터 가져와 다양한 그래프 시각화 제공)
1. 종목 폴더 디렉토리 뷰
2. 그래프 시각화 설정 에디터
3. 그래프 캔버스
'''
class comPreChart(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '종합차트'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('종합차트')

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수평 정렬
        vlay = QVBoxLayout(widget)

        # 주문 생성 에디터 위젯 가져오기
        comPreChart = comPreChart_editor(self)
        vlay1 = QVBoxLayout()
        vlay1.addWidget(comPreChart)
        vlay.addLayout(vlay1)


class comPreChart_editor(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        #전체 레이아웃
        layout = QHBoxLayout()

        # Left Layout(vlay1 + vlay2)
        leftLayout = QHBoxLayout()

        # 거래 폴더
        vlay1 = QVBoxLayout()
        self.dir_label = QLabel('거래 폴더')
        self.dir_tree = directory_tree.DirectoryTreeView()
        self.column_label = QLabel('컬럼 리스트')
        # 컬럼 리스트 트리 박스 파일 생성해야 할듯.....
        self.column_tree = QTreeView()

        vlay1.addWidget(self.dir_label)
        vlay1.addWidget(self.dir_tree)
        vlay1.addWidget(self.column_label)
        vlay1.addWidget(self.column_tree)
        leftLayout.addLayout(vlay1)

        # 그래프 시각화 설정 에디터(내부파일, 외부파일, 합성 및 병렬 라디오버튼, 그래프 추가 및 초기화 버튼)
        vlay2 = QVBoxLayout()
        # 내부파일 그룹박스
        self.innerFileGroup = QGroupBox('내부파일')
        self.innerFileGroup.setCheckable(True)
        self.innerFileGroup.setChecked(False)

        self.innerFileEdit = QLineEdit()
        self.innerFileBtn = QPushButton('선택')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.innerFileEdit)
        hbox1.addWidget(self.innerFileBtn)
        self.innerFileGroup.setLayout(hbox1)

        # 외부파일 그룹박스
        self.outerFileGroup = QGroupBox('외부파일')
        self.outerFileGroup.setCheckable(True)
        self.outerFileGroup.setChecked(False)

        self.outerFileEdit = QLineEdit()
        self.outerFileBtn = QPushButton('선택')

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.outerFileEdit)
        hbox2.addWidget(self.outerFileBtn)
        self.outerFileGroup.setLayout(hbox2)

        # 합성 및 병렬 라디오버튼
        hlay = QHBoxLayout()
        self.mergeRadio = QRadioButton('합성')
        self.parallelRadio = QRadioButton('병렬')
        hlay.addWidget(self.mergeRadio)
        hlay.addWidget(self.parallelRadio)

        self.graph_add_btn = QPushButton('그래프 추가')
        self.graph_init_btn = QPushButton('그래프 초기화')

        vlay2.addWidget(self.innerFileGroup)
        vlay2.addWidget(self.outerFileGroup)
        vlay2.addLayout(hlay)
        vlay2.addWidget(self.graph_add_btn)
        vlay2.addWidget(self.graph_init_btn)
        leftLayout.addLayout(vlay2)

        # right layout 수익률 그래프 위젯
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


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = comPreChart()
    mainWin.show()
    sys.exit(app.exec_())