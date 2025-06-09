
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


def close_all_positions(api):
    # 步骤1：创建目标持仓任务（引用slice4的TargetPosTask用法）
    tasks = {}
    for symbol in api.get_position():
        tasks[symbol] = TargetPosTask(api, symbol)

    # 步骤2：设置所有持仓目标为0（引用slice1的锁仓处理逻辑）
    for symbol, task in tasks.items():
        task.set_target_volume(0)  # 目标持仓设为0

    # 步骤3：验证平仓结果（引用slice3的持仓检查逻辑）
    while True:
        api.wait_update()
        all_closed = True
        for pos in api.get_position().values():
            if pos.pos_long != 0 or pos.pos_short != 0:
                all_closed = False
                break
        if all_closed:
            break


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



if __name__ == '__main__':
    close_all_positions(api)
