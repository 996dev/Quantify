import os
from datetime import datetime

from tqsdk.objs import Account, Position


def log_info(info):
    dirs = '../log_info/'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    with open(dirs + "log" + ".txt", "a", encoding='utf-8') as file:
        file.write(f"{info}\n")
        file.write(f"{'-' * 40}\n")


def log(symbol, account: Account, position: Position, open_position_amount, now: datetime, real_open: bool = None,
        instrument_name: str = None):
    """本地文件写入日志，控制台打印日志"""
    dirs = '../log/'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    with open(dirs + symbol + ".txt", "a", encoding='utf-8') as file:
        file.write(f"警告⚠️->：{'实盘' if real_open else '模拟'}\n")
        file.write(f"账户情况# {account}\n")
        file.write(f"账户权益# {account.balance}\n")
        file.write(f"浮动盈亏# {account.float_profit}\n")
        file.write(f"本交易日内平仓盈亏# {account.close_profit}\n")
        file.write(f"本交易日内交纳的手续费# {account.commission}\n")
        file.write(f"冻结手续费# {account.frozen_commission}\n")
        file.write(f"手续费# {account.commission}\n")
        file.write(f"保证金占用# {account.margin}\n")
        file.write(f"风险度# {'{:.2%}'.format(account.risk_ratio)}")
        file.write(f"持仓情况# {position}\n")
        file.write(f"持仓情况 浮动盈亏# {position.float_profit}\n")
        file.write(f"持仓情况 多头持仓手数# {position.pos_long}\n")
        file.write(f"持仓情况 空头持仓手数# {position.pos_short}\n")
        file.write(f"持仓情况 净持仓手数# {position.pos}\n")
        file.write(f"持仓情况 多头开仓均价# {position.open_price_long}")
        file.write(f"持仓情况 空头开仓均价# {position.open_price_short}")
        file.write(f"{symbol} {instrument_name} 开仓数量# {open_position_amount}\n")
        file.write(f"当前时间# {now}\n")
        file.write(f"{'-' * 40}\n")

        print(f"警告⚠️->: {'实盘' if real_open else '模拟'}")
        print(f"账户情况# {account}")
        print(f"账户权益# {account.balance}")
        print(f"浮动盈亏# {account.float_profit}")
        print(f"本交易日内平仓盈亏# {account.close_profit}")
        print(f"本交易日内交纳的手续费# {account.commission}")
        print(f"冻结手续费# {account.frozen_commission}")
        print(f"手续费# {account.commission}")
        print(f"保证金占用# {account.margin}")
        print(f"风险度# {'{:.2%}'.format(account.risk_ratio)}")
        print(f"持仓情况# {position}")
        print(f"持仓情况 浮动盈亏# {position.float_profit}")
        print(f"持仓情况 多头持仓手数# {position.pos_long}")
        print(f"持仓情况 空头持仓手数# {position.pos_short}")
        print(f"持仓情况 净持仓手数# {position.pos}")
        print(f"持仓情况 多头开仓均价# {position.open_price_long}")
        print(f"持仓情况 空头开仓均价# {position.open_price_short}")
        print(f"{symbol} {instrument_name} 开仓数量# {open_position_amount}")
        print(f"当前时间# {now}")
        print(f"{'-' * 40}")
