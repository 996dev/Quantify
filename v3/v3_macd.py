from tqsdk.tafunc import crossup, crossdown
from datetime import date
import datetime
import pandas as pd
from tqsdk import TqApi, TqAuth, TqAccount, TargetPosTask, TqKq, TqBacktest
from tqsdk.ta import MACD, KDJ, EMA, MACD, RSI, MA
from tool.config_watcher import cfg
from tool.kline_type import Kline
from tool.k_line_status import KLineStatus, k_line_status
from tool.log import log
from tool.time_helper import now_time

from tool.logger import logger

pd.set_option('display.max_rows', None)  # 设置Pandas显示的行数
pd.set_option('display.width', None)  # 设置Pandas显示的宽度

symbol = "DCE.m2505"

auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)

if cfg.real_open:  # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:  # 策略回测
    now = datetime.datetime.now()
    api = TqApi(backtest=TqBacktest(start_dt=date(2025, 4, 11), end_dt=date(now.year, now.month, now.day)), web_gui=True, auth=auth)
else:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)

quote = api.get_quote(symbol)

k_day = api.get_kline_serial(symbol, Kline.DAILY.value)
k_m30 = api.get_kline_serial(symbol, Kline.MINUTE30.value)
k_m15 = api.get_kline_serial(symbol, Kline.MINUTE15.value)
k_m10 = api.get_kline_serial(symbol, Kline.MINUTE10.value)
k_h1 = api.get_kline_serial(symbol, Kline.HOUR1.value)
k_h2 = api.get_kline_serial(symbol, Kline.HOUR2.value)
k_m1 = api.get_kline_serial(symbol, Kline.MINUTE1.value)

k_s5 = api.get_kline_serial(symbol, Kline.SECONDS5.value, data_length=15)
k_s10 = api.get_kline_serial(symbol, Kline.SECONDS10.value, data_length=15)
k_s15 = api.get_kline_serial(symbol, Kline.SECONDS15.value, data_length=15)
k_s30 = api.get_kline_serial(symbol, Kline.SECONDS30.value, data_length=15)

macd_m30 = MACD(k_m30, 12, 26, 9)
macd_m1 = MACD(k_m1, 12, 26, 9)

kdj_day = KDJ(k_day, 9, 3, 3)
kdj_m30 = KDJ(k_m30, 9, 3, 3)
kdj_h1 = KDJ(k_h1, 9, 3, 3)
# 获取K线数据
# 初始化目标持仓任务
target_pos = TargetPosTask(api, symbol)

if __name__ == '__main__':

    while True:
        api.wait_update()

        if api.is_changing(k_s10.iloc[-1], "datetime"):
            klines = k_m10

            rsi = RSI(klines, 60)
            ma = MA(klines, 20)
            print(list(ma["ma"]))
            # print(list(rsi["rsi"]))
            # # 计算MACD指标
            #
            # # print(list(macd_m1['diff']))
            # # print(list(macd_m1['dea']))
            # # print(list(macd_m1['bar']))
            #
            # # 获取当前价格
            # # current_price = klines.close.iloc[-1]
            # # print(quote)
            #
            # # 获取入场前的最低点（做多止损）或最高点（做空止损）
            # stop_loss_long = klines.low.iloc[-10:].min()  # 最近10根K线的最低点
            # stop_loss_short = klines.high.iloc[-10:].max()  # 最近10根K线的最高点
            # dif = macd_m1['diff']
            # dea = macd_m1['dea']
            # # print(f"crossup# {list(crossup(dif, dea))}")
            # # print(f"crossdown# {list(crossdown(dif, dea))}")
            # # 做多条件：MACD金叉
            # jx = crossup(dif, dea).iloc[-1]
            # sx = crossdown(dif, dea).iloc[-1]
            # print(f"金叉：{jx} jx==1:{jx == 1} ### 死叉：{sx} sx==1:{sx == 1}")
            # if crossup(dif, dea).iloc[-1] == 1:
            #     target_pos.set_target_volume(1)  # 开多仓
            #     print(f"做多信号触发，价格：{quote.last_price}，止损点：{stop_loss_long}，止盈点：{stop_loss_long * 2}")
            #
            # # 做空条件：MACD死叉
            # elif crossdown(dif, dea).iloc[-1] == 1:
            #     target_pos.set_target_volume(-1)  # 开空仓
            #     print(f"做空信号触发，价格：{quote.last_price}，止损点：{stop_loss_short}，止盈点：{stop_loss_short * 2}")

            # 平仓条件（可选：根据止损止盈逻辑）
        # 这里可以根据实际需求添加平仓逻辑
