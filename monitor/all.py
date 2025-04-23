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
    log_info("开始了")
    ls = api.query_cont_quotes()
    print(ls)  # 全部主连合约对应的标的合约

    ls = api.query_cont_quotes(exchange_id="DCE")
    print(ls)  # 大商所主连合约对应的标的合约

    ls = api.query_cont_quotes(product_id="jd")
    print(ls)  # jd 品种主连合约对应的标的合约
    api.close()