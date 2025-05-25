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

symbol = "SHFE.ao2509"

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

            # rsi = RSI(klines, 60)
            # ma10 = MA(klines, 10)
            # ma20 = MA(klines, 20)
            # crossup(ma10, ma20)
            # print(list(ma10["ma"]))

            # 获取5日、20日均线
            ma5 = MA(klines, 5)
            ma20 = MA(klines, 20)
            print(f"{ma5}")
            # print(f"{ma20}")

            ma5_first = ma5.iloc[-1]
            ma5_second = ma5.iloc[-2]
            ma20_first = ma20.iloc[-1]
            ma20_second = ma20.iloc[-2]

            # print(f"ma5_first：{ma5_first} # ma5_second：{ma5_second}")
            # ma5_first：ma 3134.8 Name: 199, dtype: float64  # ma5_second：ma 3134.8 Name: 198, dtype: float64
            # print(f"ma20_first：{ma20_first} # ma20_second：{ma20_second}")
            # ma20_first：ma 3145.5 Name: 199, dtype: float64  # ma20_second：ma 3148.6 Name: 198, dtype: float64


            # 检测交叉信号
            # golden_cross = crossup(ma5.iloc[-1], ma20.iloc[-1])  # 金叉信号
            # death_cross = crossdown(ma5.iloc[-1], ma20.iloc[-1])  # 死叉信号
            #
            # # 交易信号执行
            # if golden_cross.iloc[-1]:
            #     print("金叉出现，开多仓")
            #     # target_pos.set_target_volume(3)
            # elif death_cross.iloc[-1]:
            #     print("死叉出现，开空仓")
            #     # target_pos.set_target_volume(-3)
            # else:
            #     print(f"不开仓 golden_cross {golden_cross}")
            #     print(f"不开仓 death_cross {death_cross}")
