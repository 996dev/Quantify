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

pd.set_option('display.max_rows', None)  # 设置Pandas显示的行数
pd.set_option('display.width', None)  # 设置Pandas显示的宽度

# 菜油
symbol = "CZCE.OI505"

auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)

if cfg.real_open:  # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:  # 策略回测
    now = datetime.datetime.now()
    api = TqApi(backtest=TqBacktest(start_dt=date(2025, 3, 20), end_dt=date(now.year, now.month, now.day)),
                web_gui=True, auth=auth)
else:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)

symbols = ['DCE.cs2507', 'CZCE.UR509', 'CZCE.PX509', 'INE.nr2506', 'SHFE.ni2505', 'CZCE.SA509', 'CFFEX.T2506', 'CZCE.PK510', 'SHFE.ru2509', 'CFFEX.TF2506', 'SHFE.fu2507',
           'CZCE.CF509', 'SHFE.ag2506', 'INE.lu2506', 'DCE.i2509', 'CFFEX.IM2506', 'DCE.l2509', 'CFFEX.IH2506', 'DCE.pg2506', 'CZCE.PR506', 'DCE.m2509', 'DCE.j2509',
           'CZCE.SM509', 'SHFE.sn2505', 'CFFEX.IC2506', 'CZCE.OI509', 'DCE.a2507', 'INE.ec2506', 'SHFE.pb2506', 'CZCE.SF506', 'CZCE.AP510', 'DCE.v2509', 'CZCE.JR509',
           'DCE.b2509', 'CZCE.SR509', 'DCE.p2509', 'DCE.jd2506', 'INE.bc2505', 'CZCE.CY507', 'CZCE.RS507', 'GFEX.lc2507', 'SHFE.sp2507', 'DCE.lh2509', 'CZCE.PM509',
           'CZCE.ZC509', 'CZCE.WH509', 'CFFEX.IF2506', 'SHFE.ao2509', 'DCE.eb2506', 'SHFE.br2506', 'CZCE.PF506', 'CZCE.LR509', 'DCE.lg2507', 'SHFE.bu2506', 'CZCE.MA509',
           'DCE.rr2506', 'SHFE.al2506', 'DCE.jm2509', 'SHFE.ss2506', 'CZCE.RM509', 'CFFEX.TL2506', 'DCE.bb2509', 'DCE.fb2505', 'DCE.eg2509', 'CFFEX.TS2506',
           'SHFE.wr2505', 'GFEX.ps2506', 'CZCE.FG509', 'GFEX.si2506', 'SHFE.rb2510', 'CZCE.SH509', 'SHFE.au2506', 'DCE.pp2509', 'CZCE.CJ509', 'INE.sc2506', 'CZCE.RI509',
           'SHFE.hc2510', 'SHFE.zn2506', 'DCE.y2509', 'CZCE.TA509', 'SHFE.cu2506', 'DCE.c2507']

quote_list = api.get_quote_list(symbols)

k_day = api.get_kline_serial(symbols, Kline.DAILY.value, data_length=15)
k_m30 = api.get_kline_serial(symbols, Kline.MINUTE30.value, data_length=15)
k_m15 = api.get_kline_serial(symbols, Kline.MINUTE15.value, data_length=15)
k_h1 = api.get_kline_serial(symbols, Kline.HOUR1.value, data_length=15)
k_h2 = api.get_kline_serial(symbols, Kline.HOUR2.value, data_length=15)
k_h4 = api.get_kline_serial(symbols, Kline.HOUR4.value, data_length=15)
k_m1 = api.get_kline_serial(symbols, Kline.MINUTE1.value, data_length=15)
k_s5 = api.get_kline_serial(symbols, Kline.SECONDS5.value, data_length=15)
k_s10 = api.get_kline_serial(symbols, Kline.SECONDS10.value, data_length=15)
k_s15 = api.get_kline_serial(symbols, Kline.SECONDS15.value, data_length=15)
k_s30 = api.get_kline_serial(symbols, Kline.SECONDS30.value, data_length=15)

# macd_day = MACD(k_day, 12, 26, 9)
# macd_m30 = MACD(k_m30, 12, 26, 9)
#
# kdj_day = KDJ(k_day, 9, 3, 3)
# kdj_m30 = KDJ(k_m30, 9, 3, 3)
# kdj_h1 = KDJ(k_h1, 9, 3, 3)

account = api.get_account()
# position = api.get_position(symbol)
# target_pos = TargetPosTask(api, symbol)

if __name__ == '__main__':
    log_info("开始了")
    while True:
        api.wait_update()
        if api.is_changing(k_m15.iloc[-1], "datetime"):
            log_info(quote_list)
            log_info(k_h4)
            print(f"{quote_list}")
            print(f"{k_h4}")
            print(f"{'-' * 40}")
