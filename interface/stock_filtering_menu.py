import PySide2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import os
import sys
import pandas as pd

from p407_gui.interface import directory_tree, graph_canvas
from p407_gui.module.handling_file import get_refined_path

'''
종목 필터링 화면 (상장되어 있는 모든 종목 사용자 전략에 맞추어 필터링)
'''
class filtering(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = '종목필터링'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 하단 상태바
        self.statusBar().showMessage('종목필터링')

        # 메인 창 전체 레이아웃 위젯 변수 선언 및 중앙 배치
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # 메인 창 전체 레이아웃 수평 정렬
        vlay = QVBoxLayout(widget)

        # 종목 필터링 에디터 위젯 가져오기
        filtering = filtering_editor(self)
        vlay1 = QVBoxLayout()
        vlay1.addWidget(filtering)
        vlay.addLayout(vlay1)


class filtering_editor(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        #전체 레이아웃
        layout = QHBoxLayout()

        # Left Layout(vlay1)
        leftLayout = QHBoxLayout()

        # 종목이름 검색 & 전체선택 체크버튼 & 종목폴더(상장된 주가 종목 리스트 받아옴) & 전략폴더
        vlay1 = QVBoxLayout()

        # 종목 이름 리스트
        code_data = pd.read_csv('stock_data.csv', dtype={'종목코드': str}, encoding='cp949')
        code_data = code_data[['종목코드', '종목명']]
        code_data = code_data.values.tolist()
        widget_names = []
        for i in code_data:
            stock_names = ' '.join(i)
            widget_names.append(stock_names)
        self.widgets = []

        # 종목 이름 검색
        stock_hlay = QHBoxLayout()
        self.stock_name = QLabel('종목이름')

        self.stock_name_edit = QLineEdit()
        self.stock_name_edit.textChanged.connect(self.update_display)
        # 검색어 자동완성
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.stock_name_edit.setCompleter(self.completer)

        # 종목 추가 버튼
        self.stock_add_btn = QPushButton('추가')

        stock_hlay.addWidget(self.stock_name)
        stock_hlay.addWidget(self.stock_name_edit)
        stock_hlay.addWidget(self.stock_add_btn)

        # 전체선택 체크
        self.stock_check_all = QCheckBox('전체선택')

        # 종목폴더 리스트
        self.stock_label = QLabel('종목폴더')
        self.stock_list = QListWidget()
        for name in widget_names:
            self.stock_list.addItem(name)

        # 스크롤 설정
        scroll_bar = QScrollBar(self)
        self.stock_list.setVerticalScrollBar(scroll_bar)

        # 전략폴더 디렉토리 파일 뷰
        self.strategy_label = QLabel('전략폴더')
        self.strategy_tree = QTreeView()

        vlay1.addLayout(stock_hlay)
        vlay1.addWidget(self.stock_check_all)
        vlay1.addWidget(self.stock_label)
        vlay1.addWidget(self.stock_list)
        vlay1.addWidget(self.strategy_label)
        vlay1.addWidget(self.strategy_tree)
        leftLayout.addLayout(vlay1)

        # right layout (전략 파일 에디터, 파일 추가 버튼, 실행 버튼)
        self.rightLayout = QVBoxLayout()
        # 전략 파일 에디터
        self.strategy_hlay = QHBoxLayout()
        self.strategy_label = QLabel('전략 파일')
        self.strategy_edit = QLineEdit()
        self.strategy_add_btn = QPushButton('추가')
        self.filter_exec = QPushButton('실행')
        self.filter_exec.clicked.connect(self.changeWidget)

        self.strategy_hlay.addWidget(self.strategy_label)
        self.strategy_hlay.addWidget(self.strategy_edit)
        self.strategy_hlay.addWidget(self.strategy_add_btn)
        self.strategy_hlay.addWidget(self.filter_exec)

        # 추가버튼 클릭 시 전략 텍스트 띄움, 실행버튼 클릭 시 종목 매매 목록 표 띄움
        self.strategy_text = QPlainTextEdit()
        self.stock_trading_list = QTableWidget()
        # 표의 크기를 지정
        self.stock_trading_list.setColumnCount(3)
        self.stock_trading_list.setRowCount(1)
        # 열 제목 지정
        self.stock_trading_list.setHorizontalHeaderLabels(['거래일자', '종목명', '수익률'])
        # 통계자료표 내용
        self.stock_trading_list.setItem(0, 0, QTableWidgetItem('2021-01-01'))
        self.stock_trading_list.setItem(0, 1, QTableWidgetItem('삼성전자'))
        self.stock_trading_list.setItem(0, 2, QTableWidgetItem('1000%'))

        self.rightLayout.addLayout(self.strategy_hlay)
        self.rightLayout.addWidget(self.strategy_text)

        # 전체 레이아웃 병합 및 조정
        layout.addLayout(leftLayout)
        layout.addLayout(self.rightLayout)
        layout.setStretchFactor(leftLayout, 0)
        layout.setStretchFactor(self.rightLayout, 1)
        self.setLayout(layout)

    # 검색어 자동완성 시 입력 에디터 하단에 생성되는 검색어 표시줄
    def update_display(self, text):
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    # 실행 버튼 클릭 시 위젯 전환
    def changeWidget(self):
        self.rightLayout.removeWidget(self.strategy_text)
        self.strategy_text.deleteLater()
        self.rightLayout.addWidget(self.stock_trading_list)


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = filtering()
    mainWin.show()
    sys.exit(app.exec_())