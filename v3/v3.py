from datetime import date
import datetime
import pandas as pd
from tqsdk import TqApi, TqAuth, TqAccount, TargetPosTask, TqKq, TqBacktest
from tqsdk.ta import MACD, KDJ, EMA, MACD, RSI
from tool.config_watcher import cfg
from tool.kline_type import Kline
from tool.k_line_status import KLineStatus, k_line_status
from tool.log import log
from tool.time_helper import now_time

from tool.logger import logger

pd.set_option('display.max_rows', None)  # 设置Pandas显示的行数
pd.set_option('display.width', None)  # 设置Pandas显示的宽度

symbol = "CZCE.MA505"

auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)

if cfg.real_open:  # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:  # 策略回测
    now = datetime.datetime.now()
    api = TqApi(backtest=TqBacktest(start_dt=date(2025, 1, 10), end_dt=date(now.year, now.month, now.day)), web_gui=True, auth=auth)
else:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)

quote = api.get_quote(symbol)

k_day = api.get_kline_serial(symbol, Kline.DAILY.value)
k_m30 = api.get_kline_serial(symbol, Kline.MINUTE30.value)
k_m15 = api.get_kline_serial(symbol, Kline.MINUTE15.value)
k_h1 = api.get_kline_serial(symbol, Kline.HOUR1.value)
k_h2 = api.get_kline_serial(symbol, Kline.HOUR2.value)
k_m1 = api.get_kline_serial(symbol, Kline.MINUTE1.value)

macd_day = MACD(k_day, 12, 26, 9)
macd_m30 = MACD(k_m30, 12, 26, 9)

kdj_day = KDJ(k_day, 9, 3, 3)
kdj_m30 = KDJ(k_m30, 9, 3, 3)
kdj_h1 = KDJ(k_h1, 9, 3, 3)

account = api.get_account()
position = api.get_position(symbol)
target_pos = TargetPosTask(api, symbol)

klines = k_m30

# 计算指标
ema = EMA(klines, 200)  # 200日EMA
macd = MACD(klines, 12, 26, 9)  # MACD指标
rsi = RSI(klines, 50)  # RSI指标

if __name__ == '__main__':

    # 策略逻辑
    while True:
        api.wait_update()

        macd = MACD(klines, 12, 26, 9)  # 计算 MACD 指标
        # 输出结果
        print("DIF:", list(macd["diff"]))
        print("DEA:", list(macd["dea"]))
        print("BAR:", list(macd["bar"]))

        if api.is_changing(k_m1.iloc[-1], "datetime"):
            current_close = klines.close.iloc[-1]
            ema_200 = ema["ema"].iloc[-1]
            dif = macd["diff"].iloc[-1]
            dea = macd["dea"].iloc[-1]
            rsi_value = rsi.iloc[-1]
            print(f"current_close:{current_close} ema_200:{ema_200} dif:{dif} dea:{dea} rsi_value:{rsi_value}", ema_200, dif, dea, rsi_value)

            print(f"ema 200 # {current_close > ema_200}")
            print(f"MACD黄金交叉 # {dif > dea}")
            s = macd["diff"].iloc[-2] <= macd["dea"].iloc[-2]
            print(f"MACD黄金交叉 # {s}")
            print(f"RSI # {rsi_value >= 50}")
            # 做多条件
            if current_close > ema_200 and dif > dea and macd["diff"].iloc[-2] <= macd["dea"].iloc[-2] and rsi_value >= 50:
                # 股价在200EMA以上  MACD黄金交叉 RSI >= 50
                print("满足做多条件，开仓做多")
                stop_loss = klines.low.iloc[-1]  # 止损点为前低
                take_profit = current_close + 2 * (current_close - stop_loss)  # 止盈点为止损点的两倍
                # 实际交易逻辑（示例）
                # order = api.insert_order(symbol, direction="BUY", offset="OPEN", volume=1)
                print(f"止损点: {stop_loss}, 止盈点: {take_profit}")

            # 做空条件 # 股价在200EMA以下 # MACD死亡交叉  # RSI < 50
            elif current_close < ema_200 and dif < dea and macd["diff"].iloc[-2] >= macd["dea"].iloc[-2] and rsi_value < 50:
                print("满足做空条件，开仓做空")
                stop_loss = klines.high.iloc[-1]  # 止损点为前高
                take_profit = current_close - 2 * (stop_loss - current_close)  # 止盈点为止损点的两倍
                # 实际交易逻辑（示例）
                # order = api.insert_order(symbol, direction="SELL", offset="OPEN", volume=1)
                print(f"止损点: {stop_loss}, 止盈点: {take_profit}")

    # 关闭API
    api.close()
