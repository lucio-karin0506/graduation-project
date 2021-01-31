from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2
import os
import sys
import pandas as pd

from p407_gui.module import label_indicator

'''
다이얼로그
1. 볼린저밴드 레이블 파라미터 설정 다이얼로그
'''
class bbands_label_Param(QDialog):
    def __init__(self, title, path, parent):
        super().__init__(parent)
        self.path = path

        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400

        self.setWindowTitle(title + ' 파라미터 설정')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()

        layout = QVBoxLayout()
        hlay1 = QHBoxLayout()
        hlay2 = QHBoxLayout()
        hlay3 = QHBoxLayout()
        hlay4 = QHBoxLayout()

        self.target_label = QLabel('레이블 대상', self)
        self.target_option = QComboBox(self)
        self.target_option.addItem('종가', 'close')
        self.target_option.addItem('시가', 'open')
        self.target_option.addItem('고가', 'high')
        self.target_option.addItem('저가', 'low')

        self.period_label = QLabel('이평기간', self)
        self.period_edit = QLineEdit(self)
        self.period_edit.setPlaceholderText('20')

        self.multid_label = QLabel('표준편차배수', self)
        self.multid_edit = QLineEdit(self)
        self.multid_edit.setPlaceholderText('2')

        self.confirm_btn = QPushButton('확인', self)
        self.confirm_btn.clicked.connect(self.confirmIt)
        self.close_btn = QPushButton('취소', self)
        self.close_btn.clicked.connect(self.closeIt)

        hlay1.addWidget(self.target_label)
        hlay1.addWidget(self.target_option)
        hlay2.addWidget(self.period_label)
        hlay2.addWidget(self.period_edit)
        hlay3.addWidget(self.multid_label)
        hlay3.addWidget(self.multid_edit)
        hlay4.addWidget(self.confirm_btn)
        hlay4.addWidget(self.close_btn)

        layout.addLayout(hlay1)
        layout.addLayout(hlay2)
        layout.addLayout(hlay3)
        layout.addLayout(hlay4)
        self.setLayout(layout)

    def confirmIt(self):
        # 1. 기존 csv 파일에 지표 컬럼 추가
        df = pd.read_csv(self.path, index_col='Date')
        gathering_info = {'df': df,
                          'period': int(self.period_edit.text()),
                          'multid': int(self.multid_edit.text()),
                          'target': str(self.target_option.currentData())
                          }

        label_indicator.bbands(gathering_info['df'], gathering_info['period'], gathering_info['multid'],
                                   gathering_info['target'])
        gathering_info['df'].to_csv(self.path, index_label='Date')

        msg = QMessageBox.information(self, "메시지", "파라미터 설정이 완료되었습니다!", QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            bbands_label_Param.close(self)
        # 2. 그래프 생성
        # 3. 지표 리스트에 지표 목록 생성

    # 화면 중앙 배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeIt(self):
        bbands_label_Param.close(self)

    def showModal(self):
        return super().exec_()