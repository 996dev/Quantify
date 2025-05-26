from datetime import date
import datetime
import pandas as pd
from tqsdk import TqApi, TqAuth, TqAccount, TargetPosTask, TqKq, TqBacktest
from tqsdk.ta import MACD, KDJ

from tool.config_watcher import cfg
from tool.kline_type import Kline
from tool.k_line_status import KLineStatus, k_line_status
from tool.log import log, log_info
from tool.time_helper import now_time

from tool.logger import logger

auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)

if cfg.real_open:  # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:  # 策略回测
    now = datetime.datetime.now()
    api = TqApi(backtest=TqBacktest(start_dt=date(2025, 1, 20), end_dt=date(now.year, now.month, now.day)),
                web_gui=True, auth=auth)
else:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)

# contracts = api.query_cont_quotes()  # 获取所有合约

if __name__ == '__main__':
    list_night = []
    list_today = []
    dce = api.query_cont_quotes(exchange_id="DCE")
    dce_night = api.query_cont_quotes(exchange_id="DCE", has_night=True)
    dce_day = api.query_cont_quotes(exchange_id="DCE", has_night=False)
    list_night.extend(dce_night)
    list_today.extend(dce_day)
    print(f"大商所 夜盘 {dce_night}")
    print(f"大商所 无夜盘 {dce_day}")

    ls = api.query_cont_quotes(exchange_id="SHFE")
    shfe_night = api.query_cont_quotes(exchange_id="SHFE", has_night=True)
    shfe_day = api.query_cont_quotes(exchange_id="SHFE", has_night=False)
    list_night.extend(shfe_night)
    list_today.extend(shfe_day)
    print(f"上期所 {ls}")
    print(f"上期所 夜盘 {shfe_night}")
    print(f"上期所 无夜盘 {shfe_day}")

    ls = api.query_cont_quotes(exchange_id="CZCE")
    czce_night = api.query_cont_quotes(exchange_id="CZCE", has_night=True)
    czce_day = api.query_cont_quotes(exchange_id="CZCE", has_night=False)
    list_night.extend(czce_night)
    list_today.extend(czce_day)
    print(f"郑商所 {ls}")
    print(f"郑商所 夜盘 {czce_night}")
    print(f"郑商所 无夜盘 {czce_day}")

    ls = api.query_cont_quotes(exchange_id="INE")
    ine_night = api.query_cont_quotes(exchange_id="INE", has_night=True)
    ine_day = api.query_cont_quotes(exchange_id="INE", has_night=False)
    list_night.extend(ine_night)
    list_today.extend(ine_day)
    print(f"能源交易所(原油) {ls}")
    print(f"能源交易所 夜盘 {ine_night}")
    print(f"能源交易所 无夜盘 {ine_day}")

    ls = api.query_cont_quotes(exchange_id="GFEX")
    gfex_night = api.query_cont_quotes(exchange_id="GFEX", has_night=True)
    gfex_day = api.query_cont_quotes(exchange_id="GFEX", has_night=False)
    list_night.extend(gfex_night)
    list_today.extend(gfex_day)
    print(f"广州期货交易所 {ls}")
    print(f"广州期货交易所 夜盘 {gfex_night}")
    print(f"广州期货交易所 无夜盘 {gfex_day}")

    print(f"夜盘 {list_night}")
    print(f"无夜盘 {list_today}")

    api.close()
