from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2
import os
import sys
import pandas as pd

from p407_gui.module import indicator

'''
다이얼로그
1. stochastic slow 파라미터 설정 다이얼로그
'''
class stoch_slow_Param(QDialog):
    def __init__(self, title, path, parent):
        super().__init__(parent)
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400

        self.path = path

        self.setWindowTitle(title + ' 파라미터 설정')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()

        layout = QVBoxLayout()
        hlay1 = QHBoxLayout()
        hlay2 = QHBoxLayout()
        hlay3 = QHBoxLayout()
        hlay4 = QHBoxLayout()
        hlay5 = QHBoxLayout()
        hlay6 = QHBoxLayout()
        hlay7 = QHBoxLayout()

        self.price1_label = QLabel('가격 종류1')
        self.price1_option = QComboBox(self)
        self.price1_option.addItem('종가', 'close')
        self.price1_option.addItem('시가', 'open')
        self.price1_option.addItem('고가', 'high')
        self.price1_option.addItem('저가', 'low')

        self.price2_label = QLabel('가격 종류2')
        self.price2_option = QComboBox(self)
        self.price2_option.addItem('종가', 'close')
        self.price2_option.addItem('시가', 'open')
        self.price2_option.addItem('고가', 'high')
        self.price2_option.addItem('저가', 'low')

        self.price3_label = QLabel('가격 종류3')
        self.price3_option = QComboBox(self)
        self.price3_option.addItem('종가', 'close')
        self.price3_option.addItem('시가', 'open')
        self.price3_option.addItem('고가', 'high')
        self.price3_option.addItem('저가', 'low')

        self.fastk_label = QLabel('fastk_period')
        self.fastk_edit = QLineEdit()
        self.fastk_edit.setPlaceholderText('5')

        self.slowk_label = QLabel('slowk_period')
        self.slowk_edit = QLineEdit()
        self.slowk_edit.setPlaceholderText('3')

        self.slowd_label = QLabel('slowd_period')
        self.slowd_edit = QLineEdit()
        self.slowd_edit.setPlaceholderText('3')

        self.confirm_btn = QPushButton('확인')
        self.confirm_btn.clicked.connect(self.confirmIt)
        self.close_btn = QPushButton('취소')
        self.close_btn.clicked.connect(self.closeIt)

        hlay1.addWidget(self.price1_label)
        hlay1.addWidget(self.price1_option)

        hlay2.addWidget(self.price2_label)
        hlay2.addWidget(self.price2_option)

        hlay3.addWidget(self.price3_label)
        hlay3.addWidget(self.price3_option)

        hlay4.addWidget(self.fastk_label)
        hlay4.addWidget(self.fastk_edit)

        hlay5.addWidget(self.slowk_label)
        hlay5.addWidget(self.slowk_edit)

        hlay6.addWidget(self.slowd_label)
        hlay6.addWidget(self.slowd_edit)

        hlay7.addWidget(self.confirm_btn)
        hlay7.addWidget(self.close_btn)

        layout.addLayout(hlay1)
        layout.addLayout(hlay2)
        layout.addLayout(hlay3)
        layout.addLayout(hlay4)
        layout.addLayout(hlay5)
        layout.addLayout(hlay6)
        layout.addLayout(hlay7)
        self.setLayout(layout)

    def confirmIt(self):
        # 1. 기존 csv 파일에 지표 컬럼 추가
        df = pd.read_csv(self.path, index_col='Date')
        gathering_info = {'df': df,
                          'fastk_period': int(self.fastk_edit.text()),
                          'slowk_period': int(self.slowk_edit.text()),
                          'slowd_period': int(self.slowd_edit.text()),
                          'price1': str(self.price1_option.currentData()),
                          'price2': str(self.price2_option.currentData()),
                          'price3': str(self.price3_option.currentData())
                          }

        indicator.add_STOCH(gathering_info['df'], gathering_info['fastk_period'], gathering_info['slowk_period'],
                             gathering_info['slowd_period'],
                             gathering_info['price1'], gathering_info['price2'], gathering_info['price3'])
        gathering_info['df'].to_csv(self.path, index_label='Date')

        msg = QMessageBox.information(self, "메시지", "파라미터 설정이 완료되었습니다!", QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            stoch_slow_Param.close(self)
        # 2. 그래프 생성
        # 3. 지표 리스트에 지표 목록 생성

    # 화면 중앙 배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeIt(self):
        stoch_slow_Param.close(self)

    def showModal(self):
        return super().exec_()