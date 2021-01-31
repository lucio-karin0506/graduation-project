import PySide2
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import os
import sys

from p407_gui.interface import directory_tree, indicator_tree

'''
주문 생성 화면
1. 주문 생성 에디터
2. 디버그 로깅 창
'''
class simple_strategy(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '단순전략'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('단순전략')

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수평 정렬
        vlay = QVBoxLayout(widget)

        # 주문 생성 에디터 위젯 가져오기
        order_create = order_editor(self)
        vlay1 = QVBoxLayout()
        vlay1.addWidget(order_create)
        vlay.addLayout(vlay1)


class order_editor(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        #전체 레이아웃
        layout = QHBoxLayout()

        # Left Layout(데이터 불러오기 옵션 라디오버튼, directory tree, 지표 리스트)
        leftLayout = QVBoxLayout()

        # 데이터 불러오는 옵션 라디오 버튼
        optionLayout = QHBoxLayout()
        self.local_Mode = QRadioButton('로컬파일모드')
        self.local_Mode.setChecked(False)
        self.net_Mode = QRadioButton('네트워크모드')
        self.net_Mode.setChecked(False)
        optionLayout.addWidget(self.local_Mode)
        optionLayout.addWidget(self.net_Mode)

        self.dir_label = QLabel('종목폴더')
        self.dir_tree = directory_tree.DirectoryTreeView()
        self.tech_label = QLabel('지표')
        self.tech_tree = indicator_tree.IndicatorTreeView()

        leftLayout.addLayout(optionLayout)
        leftLayout.addWidget(self.dir_label)
        leftLayout.addWidget(self.dir_tree)
        leftLayout.addWidget(self.tech_label)
        leftLayout.addWidget(self.tech_tree)

        # right Layout(주문 생성 정보 입력, 에디터)
        rightLayout = QVBoxLayout()

        # 주문기간, 봉 타입, 적용 종목(라디오버튼)
        inputLayout = QVBoxLayout()

        # 적용 종목
        periodLayout = QHBoxLayout()

        self.stock_use_label = QLabel('적용종목')
        self.stock_use_edit = QLineEdit()
        hlay = QHBoxLayout()
        hlay.addWidget(self.stock_use_label)
        hlay.addWidget(self.stock_use_edit)
        periodLayout.addLayout(hlay)

        # 주문기간
        self.order_period_label = QLabel('운용 기간')
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate(2020, 1, 1))
        self.start_date.setDisplayFormat('yyyy-MM-dd')
        self.start_date.setCalendarPopup(True)
        self.order_interval = QLabel('~')
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate(2021, 1, 1))
        self.end_date.setDisplayFormat('yyyy-MM-dd')
        self.end_date.setCalendarPopup(True)

        periodLayout.addWidget(self.order_period_label)
        periodLayout.addWidget(self.start_date)
        periodLayout.addWidget(self.order_interval)
        periodLayout.addWidget(self.end_date)

        inputLayout.addLayout(periodLayout)
        rightLayout.addLayout(inputLayout)

        # 입력 확인 버튼
        self.stock_info_check = QPushButton('입력 확인')
        inputLayout.addWidget(self.stock_info_check)

        # 전략 조건식, 전략 조건식 검증 버튼, 주문 생성 버튼 레이아웃
        # 전략 조건식
        self.strategy_edit_label = QLabel('거래 전략 편집기')
        self.strategy_edit_text = QPlainTextEdit()
        vlay = QVBoxLayout()
        vlay.addWidget(self.strategy_edit_label)
        vlay.addWidget(self.strategy_edit_text)
        rightLayout.addLayout(vlay)

        # 전략 조건식 검증, 주문 생성 버튼
        self.strategy_test_button = QPushButton('전략 조건식 검증')
        self.order_create_button = QPushButton('주문 생성')
        hlay3 = QHBoxLayout()
        hlay3.addWidget(self.strategy_test_button)
        hlay3.addWidget(self.order_create_button)
        rightLayout.addLayout(hlay3)
        self.strategy_test_button.clicked.connect(self.strategy_test)

        # 전체 레이아웃 병합 및 조정
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 0)
        layout.setStretchFactor(rightLayout, 1)
        self.setLayout(layout)

    def strategy_test(self):
        pass


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = simple_strategy()
    mainWin.show()
    sys.exit(app.exec_())