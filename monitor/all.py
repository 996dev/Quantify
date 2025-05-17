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
    print(f"大商所 {ls}")
    ls = api.query_cont_quotes(exchange_id="SHFE")
    print(f"上期所 {ls}")
    ls = api.query_cont_quotes(exchange_id="CZCE")
    print(f"郑商所 {ls}")
    ls = api.query_cont_quotes(exchange_id="INE")
    print(f"能源交易所(原油) {ls}")
    ls = api.query_cont_quotes(exchange_id="GFEX")
    print(f"广州期货交易所 {ls}")
    # 大商所 = [
    #     'DCE.rr2507', 'DCE.fb2506', 'DCE.pg2506', 'DCE.c2507', 'DCE.lh2509', 'DCE.l2509', 'DCE.y2509', 'DCE.jd2506', 'DCE.lg2507', 'DCE.eg2509', 'DCE.cs2507',
    #     'DCE.p2509', 'DCE.v2509', 'DCE.bb2511', 'DCE.j2509', 'DCE.b2509', 'DCE.a2507', 'DCE.eb2506', 'DCE.jm2509', 'DCE.m2509', 'DCE.i2509', 'DCE.pp2509']
    # 上期所 = [
    #     'SHFE.au2508', 'SHFE.ag2506', 'SHFE.wr2510', 'SHFE.sn2506', 'SHFE.fu2507', 'SHFE.bu2506', 'SHFE.zn2506', 'SHFE.sp2507', 'SHFE.pb2506', 'SHFE.hc2510',
    #     'SHFE.br2506', 'SHFE.cu2506', 'SHFE.ao2509', 'SHFE.ni2506', 'SHFE.rb2510', 'SHFE.ss2506', 'SHFE.ru2509', 'SHFE.al2506']
    # 郑商所 = [
    #     'CZCE.SF506', 'CZCE.LR509', 'CZCE.RS507', 'CZCE.CF509', 'CZCE.RI509', 'CZCE.CY507', 'CZCE.SM509', 'CZCE.PR507', 'CZCE.RM509', 'CZCE.AP510', 'CZCE.PK510',
    #     'CZCE.CJ509', 'CZCE.FG509', 'CZCE.SA509', 'CZCE.ZC509', 'CZCE.JR509', 'CZCE.MA509', 'CZCE.SH509', 'CZCE.OI509', 'CZCE.PF506', 'CZCE.SR509', 'CZCE.TA509',
    #     'CZCE.WH509', 'CZCE.UR509', 'CZCE.PM509', 'CZCE.PX509']
    # 能源交易所 = ['INE.sc2506', 'INE.lu2507', 'INE.nr2506', 'INE.ec2506', 'INE.bc2506']
    # 广州期货交易所 = ['GFEX.si2506', 'GFEX.ps2506', 'GFEX.lc2507']
    # *CFFEX: 中金所
    # *SHFE: 上期所
    # *DCE: 大商所
    # *CZCE: 郑商所
    # *INE: 能源交易所(原油)
    # *GFEX: 广州期货交易所
    api.close()
