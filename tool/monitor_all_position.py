from tqsdk import TqApi, TqAuth, TqSim

from datetime import date

import pandas as pd
from tqsdk import TqApi, TqAuth, TqAccount, TargetPosTask, TqKq, TqBacktest
from tqsdk.ta import MACD, KDJ

from tool.config_watcher import cfg
from tool.kline_type import Kline
from time_helper import now_time

from tool.send_email_163 import email_163

pd.set_option('display.max_rows', None)  # 设置Pandas显示的行数
pd.set_option('display.width', None)  # 设置Pandas显示的宽度
# 棉花
symbol = "CZCE.CF505"

auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)
if cfg.real_open:
    # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:
    # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:
    # 策略回测
    api = TqApi(backtest=TqBacktest(start_dt=date(2024, 8, 20), end_dt=date(2024, 12, 3)), web_gui=True, auth=auth)
else:
    # 快期模拟
    api = TqApi(TqKq(), auth=auth)
# api = TqApi(TqSim(), auth=auth)
# 实盘
# api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
# 策略回测
# api = TqApi(backtest=TqBacktest(start_dt=date(2018, 5, 1), end_dt=date(2018, 10, 1)), auth=auth)


quote = api.get_quote(symbol)

k_day = api.get_kline_serial(symbol, Kline.DAILY.value, data_length=15)
k_h2 = api.get_kline_serial(symbol, Kline.HOUR2.value, data_length=15)
k_h1 = api.get_kline_serial(symbol, Kline.HOUR1.value, data_length=15)
k_m30 = api.get_kline_serial(symbol, Kline.MINUTE30.value, data_length=15)
k_m15 = api.get_kline_serial(symbol, Kline.MINUTE15.value, data_length=15)
k_m1 = api.get_kline_serial(symbol, Kline.MINUTE1.value, data_length=15)

macd_day = MACD(k_day, 12, 26, 9)
macd_h2 = MACD(k_h2, 12, 26, 9)
macd_h1 = MACD(k_h1, 12, 26, 9)
macd_m30 = MACD(k_m30, 12, 26, 9)

kdj_day = KDJ(k_day, 9, 3, 3)
kdj_h2 = KDJ(k_h2, 9, 3, 3)
kdj_h1 = KDJ(k_h1, 9, 3, 3)
kdj_m30 = KDJ(k_m30, 9, 3, 3)

account = api.get_account()
position = api.get_position(symbol)
target_pos = TargetPosTask(api, symbol)

ls = api.query_cont_quotes()

# 全部主连合约
all_symbols = api.query_quotes(ins_class="CONT")
# 打印所有合约列表
print("所有期货合约列表：")
print(all_symbols)

symbol1 = "CZCE.CF505"
quote1 = api.get_quote(symbol1)

k_day1 = api.get_kline_serial(symbol1, Kline.DAILY.value, data_length=15)
k_h21 = api.get_kline_serial(symbol1, Kline.HOUR2.value, data_length=15)
k_h11 = api.get_kline_serial(symbol1, Kline.HOUR1.value, data_length=15)
k_m301 = api.get_kline_serial(symbol1, Kline.MINUTE30.value, data_length=15)
k_m151 = api.get_kline_serial(symbol1, Kline.MINUTE15.value, data_length=15)
k_m11 = api.get_kline_serial(symbol1, Kline.MINUTE1.value, data_length=15)

if __name__ == '__main__':

    while True:
        api.wait_update()
        if api.is_changing(k_m301.iloc[-1], "datetime"):
            # 遍历所有合约
            send_message = []
            for symbol in all_symbols:
                try:
                    # 获取合约的最新报价和日线数据
                    quote = api.get_quote(symbol)

                    upper_limit = quote.upper_limit
                    lower_limit = quote.lower_limit
                    price = quote.last_price
                    instrument_name = quote.instrument_name
                    now = now_time(quote)

                    k_day = api.get_kline_serial(symbol, Kline.DAILY.value, data_length=15)
                    k_h2 = api.get_kline_serial(symbol, Kline.HOUR2.value, data_length=15)
                    k_h1 = api.get_kline_serial(symbol, Kline.HOUR1.value, data_length=15)
                    k_m30 = api.get_kline_serial(symbol, Kline.MINUTE30.value, data_length=15)
                    k_m15 = api.get_kline_serial(symbol, Kline.MINUTE15.value, data_length=15)
                    k_m1 = api.get_kline_serial(symbol, Kline.MINUTE1.value, data_length=15)

                    # macd_day = MACD(k_day, 12, 26, 9)
                    # macd_h2 = MACD(k_h2, 12, 26, 9)
                    # macd_h1 = MACD(k_h1, 12, 26, 9)
                    # macd_m30 = MACD(k_m30, 12, 26, 9)
                    #
                    # kdj_day = KDJ(k_day, 9, 3, 3)
                    # kdj_h2 = KDJ(k_h2, 9, 3, 3)
                    # kdj_h1 = KDJ(k_h1, 9, 3, 3)
                    # kdj_m30 = KDJ(k_m30, 9, 3, 3)
                    # 获取日线开盘价
                    day_open_price = k_day.iloc[-1]['open']

                    # 打印合约信息
                    print(f"合约 {symbol} 的最新价格：{quote.last_price}")
                    print(f"合约 {symbol} 的日线开盘价：{day_open_price}")

                    # 判断当前价格与日线开盘价的关系
                    if quote.last_price > day_open_price:
                        # 当前价格大于日线开盘价，开多单
                        print(f"合约 {symbol} 开多单")
                        send_message.append(f"合约{instrument_name} {symbol} 开多单")
                    elif quote.last_price < day_open_price:
                        # 当前价格小于日线开盘价，开空单
                        print(f"合约 {symbol} 开空单")
                        send_message.append(f"合约{instrument_name} {symbol} 开空单")
                    else:
                        print(f"合约 {symbol} 当前价格等于日线开盘价，不操作")

                except Exception as e:
                    print(f"处理合约 {symbol} 时发生错误：{e}")

            email_163.send_message(send_message.__str__())
            # 关闭API
            # api.close()
