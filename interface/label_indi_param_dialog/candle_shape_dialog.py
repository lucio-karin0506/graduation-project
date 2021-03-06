import pandas as pd

from p407_gui.module import label_indicator

'''
다이얼로그
1. 캔들 종류 레이블 파라미터 설정 다이얼로그
'''

def confirmIt(path):
    # 1. 기존 csv 파일에 지표 컬럼 추가
    df = pd.read_csv(path, index_col='Date')
    gathering_info = {'df': df}

    label_indicator.candle_shape(gathering_info['df'])
    gathering_info['df'].to_csv(path, index_label='Date')
    # 2. 그래프 생성
    # 3. 지표 리스트에 지표 목록 생성