from datetime import date
import datetime
import pandas as pd
from tqsdk import TqApi, TqAuth, TqAccount, TargetPosTask, TqKq, TqBacktest
from tqsdk.ta import MACD, KDJ

from tool.config_watcher import cfg
from tool.kline_type import Kline
from tool.k_line_status import KLineStatus, k_line_status
from tool.log import log
from tool.time_helper import now_time

from tool.logger import logger

pd.set_option('display.max_rows', None)  # 设置Pandas显示的行数
pd.set_option('display.width', None)  # 设置Pandas显示的宽度

# 豆一
symbol = "SHFE.zn2508"

auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)

if cfg.real_open:  # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:  # 策略回测
    now = datetime.datetime.now()
    api = TqApi(backtest=TqBacktest(start_dt=date(2024, 8, 20), end_dt=date(now.year, now.month, now.day)),
                web_gui=True, auth=auth)
else:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)

quote = api.get_quote(symbol)

k_day = api.get_kline_serial(symbol, Kline.DAILY.value, data_length=15)
k_m30 = api.get_kline_serial(symbol, Kline.MINUTE30.value, data_length=15)
k_m15 = api.get_kline_serial(symbol, Kline.MINUTE15.value, data_length=15)
k_h1 = api.get_kline_serial(symbol, Kline.HOUR1.value, data_length=15)
k_h2 = api.get_kline_serial(symbol, Kline.HOUR2.value, data_length=15)
k_m1 = api.get_kline_serial(symbol, Kline.MINUTE1.value, data_length=15)
k_s10 = api.get_kline_serial(symbol, Kline.SECONDS10.value, data_length=15)
k_s15 = api.get_kline_serial(symbol, Kline.SECONDS15.value, data_length=15)
k_s30 = api.get_kline_serial(symbol, Kline.SECONDS30.value, data_length=15)

macd_day = MACD(k_day, 12, 26, 9)
macd_m30 = MACD(k_m30, 12, 26, 9)

kdj_day = KDJ(k_day, 9, 3, 3)
kdj_m30 = KDJ(k_m30, 9, 3, 3)
kdj_h1 = KDJ(k_h1, 9, 3, 3)

account = api.get_account()
position = api.get_position(symbol)
target_pos = TargetPosTask(api, symbol)

ls = api.query_cont_quotes()

open_position_amount = 1

if __name__ == '__main__':
    print(f"开仓数量 {open_position_amount}")
    while True:
        api.wait_update()
        upper_limit = quote.upper_limit
        lower_limit = quote.lower_limit
        last_price = quote.last_price
        instrument_name = quote.instrument_name
        now = now_time(quote)
        if api.is_changing(k_m1.iloc[-1], "datetime"):
            print(f"flast_price={last_price}")
            k_line_day = k_day.iloc[-1]
            print(f"日线 K线起始时刻的最新价：{k_line_day.open} K线结束时刻的最新价：{k_line_day.close}")
            k_line_h1 = k_h1.iloc[-1]
            print(f"1小时线 K线起始时刻的最新价：{k_line_h1.open} K线结束时刻的最新价：{k_line_h1.close}")
            k_line_m30 = k_m30.iloc[-1]
            print(f"30分钟线 K线起始时刻的最新价：{k_line_m30.open} K线结束时刻的最新价：{k_line_m30.close}")
            k_line_h2 = k_h2.iloc[-1]

            status_day = k_line_status(last_price, k_line_day.open)
            print(f"日线状态：{status_day}")
            status_h1 = k_line_status(k_line_h1.close, k_line_h1.open)
            print(f"1小时线状态：{status_h1}")
            status_m30 = k_line_status(last_price, k_line_m30.open)
            print(f"30分钟线状态：{status_m30}")
            # status = k_line_status(last_price, k_line_h2.open)
            status = status_day
            if status == KLineStatus.UPWARD:
                target_pos.set_target_volume(abs(open_position_amount))
                print(f"{instrument_name} 开多单")
            elif status == KLineStatus.FELL:
                target_pos.set_target_volume(-open_position_amount)
                print(f"{instrument_name} 开空单")
            elif status == KLineStatus.EQUAL:
                print(f"{instrument_name} 不开单")

            log(symbol, account, position, open_position_amount, now, cfg.real_open, instrument_name=instrument_name)
