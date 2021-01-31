from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2
import os
import sys
import pandas as pd

from p407_gui.module import indicator

'''
다이얼로그
1. bb 파라미터 설정 다이얼로그
'''
class bb_Param(QDialog):
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

        self.price_label = QLabel('가격 종류')
        self.price_option = QComboBox(self)
        self.price_option.addItem('종가', 'close')
        self.price_option.addItem('시가', 'open')
        self.price_option.addItem('고가', 'high')
        self.price_option.addItem('저가', 'low')

        self.period_label = QLabel('기간')
        self.period_edit = QLineEdit()
        self.period_edit.setPlaceholderText('20')

        self.up_label = QLabel('nbdevup')
        self.up_edit = QLineEdit()

        self.up_edit.setPlaceholderText('2')
        self.down_label = QLabel('nbdevdn')

        self.down_edit = QLineEdit()
        self.down_edit.setPlaceholderText('2')

        self.confirm_btn = QPushButton('확인')
        self.confirm_btn.clicked.connect(self.confirmIt)
        self.close_btn = QPushButton('취소')
        self.close_btn.clicked.connect(self.closeIt)

        hlay1.addWidget(self.price_label)
        hlay1.addWidget(self.price_option)
        hlay2.addWidget(self.period_label)
        hlay2.addWidget(self.period_edit)
        hlay3.addWidget(self.up_label)
        hlay3.addWidget(self.up_edit)
        hlay4.addWidget(self.down_label)
        hlay4.addWidget(self.down_edit)
        hlay5.addWidget(self.confirm_btn)
        hlay5.addWidget(self.close_btn)

        layout.addLayout(hlay1)
        layout.addLayout(hlay2)
        layout.addLayout(hlay3)
        layout.addLayout(hlay4)
        layout.addLayout(hlay5)
        self.setLayout(layout)

    def confirmIt(self):
        # 1. 기존 csv 파일에 지표 컬럼 추가
        df = pd.read_csv(self.path, index_col='Date')
        gathering_info = {'df': df,
                          'period': int(self.period_edit.text()),
                          'nbdevup': int(self.up_edit.text()),
                          'nbdevdn': int(self.down_edit.text()),
                          'price': str(self.price_option.currentData())
                         }

        indicator.add_BBands(gathering_info['df'], gathering_info['period'], gathering_info['nbdevup'],
                         gathering_info['nbdevdn'], gathering_info['price'])
        gathering_info['df'].to_csv(self.path, index_label='Date')

        msg = QMessageBox.information(self, "메시지", "파라미터 설정이 완료되었습니다!", QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            bb_Param.close(self)
        # 2. 그래프 생성

    # 화면 중앙 배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeIt(self):
        bb_Param.close(self)

    def showModal(self):
        return super().exec_()