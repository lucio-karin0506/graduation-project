import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from mplfinance.original_flavor import candlestick2_ohlc
import pandas as pd
import copy

class draw_ma():
    def draw_ma(self, df, period):
        copy_df = copy.deepcopy(df)
        copy_df.reset_index(inplace=True)

        # print('test')
        # print(df)
        # print(period)
        # indicator.add_MA(copy_df, period, price)

        # 한글 폰트 지정
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
        fig, ax = plt.subplots(figsize=(12, 10))

        # x-축 날짜
        xdate = copy_df.Date.astype('str')
        for i in range(len(xdate)):
            xdate[i] = xdate[i][2:]  # 2020-01-01 => 20-01-01

        # 이동평균선 차트
        # if state == 'ma':
        #     self.axes[0].plot(xdate, copy_df['ma_' + str(period)], 'g-', label='MA' + str(period))

        # 기본차트
        # ax.plot(xdate, copy_df[price], 'k-')
        candlestick2_ohlc(self.axes[0], copy_df['open'], copy_df['high'],
                          copy_df['low'], copy_df['close'], width=0.6, colorup='r', colordown='b')

        # self.fig.set_title('Stock Chart', fontsize=20)
        self.fig.autofmt_xdate(rotation=45)
        self.axes[0].set_xlabel("Date")
        self.axes[0].set_ylabel("Price")
        self.axes[0].xaxis.set_major_locator(ticker.MaxNLocator(25))
        self.axes[0].legend(loc='best') # legend 위치
        self.axes[0].grid()

        # plt.xticks(rotation=45)  # x-축 글씨 45도 회전
        # plt.grid()  # 그리드 표시
        # plt.show()

        scale = 1.1
        self.zoom_factory(self.axes[0], base_scale=scale)
        self.pan_factory(self.axes[0])

        self.draw()


# if __name__ == "__main__":
#
#     mod = Gathering()
#     df = mod.get_stock('000660', '2020-01-01', '2021-01-01', 'D')
#
#     # print(df)
#     draw_ma(df, 5, 'close')