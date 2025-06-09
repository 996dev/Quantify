from tqsdk import TqApi, TqAuth, TqSim, TargetPosTask
import pandas as pd
import numpy as np

# 初始化账户（免费版使用TqSim模拟账户）
account = TqSim()
api = TqApi(account, auth=TqAuth("快期账户", "密码"))

# 参数优化区间（需自行回测）
params = {
    "macd_fast": [10, 12, 14],
    "macd_slow": [24, 26, 28],
    "kdj_n": [7, 9, 11],
    "overbought": [75, 80, 85],
    "oversold": [15, 20, 25]
}

# 获取螺纹钢主力合约数据
symbol = "SHFE.rb2409"
klines = api.get_kline_serial(symbol, 900, 5000)


def calc_macd(close, fast=12, slow=26, signal=9):
    """MACD计算函数（slice1提到MACD基础实现）"""
    ema_fast = close.ewm(span=fast).mean()
    ema_slow = close.ewm(span=slow).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal).mean()
    macd = (dif - dea) * 2
    return dif, dea, macd


def calc_kdj(high, low, close, n=9, m=3):
    """KDJ计算函数（结合slice3的K线数据获取逻辑）"""
    lowest = low.rolling(n).min()
    highest = high.rolling(n).max()
    rsv = (close - lowest) / (highest - lowest) * 100
    k = rsv.ewm(alpha=1 / m).mean()
    d = k.ewm(alpha=1 / m).mean()
    j = 3 * k - 2 * d
    return k, d, j


# 计算双指标
dif, dea, macd = calc_macd(klines.close)
k, d, j = calc_kdj(klines.high, klines.low, klines.close)

# 交易信号生成（slice2提到信号触发逻辑）
position = TargetPosTask(api, symbol)
while True:
    api.wait_update()
    latest = klines.iloc[-1]

    # MACD金叉 + KDJ超卖
    if (dif.iloc[-1] > dea.iloc[-1]) and (dif.iloc[-2] <= dea.iloc[-2]) and (j.iloc[-1] < 20):
        position.set_target_volume(3)  # 开多3手

    # MACD死叉 + KDJ超买
    elif (dif.iloc[-1] < dea.iloc[-1]) and (dif.iloc[-2] >= dea.iloc[-2]) and (j.iloc[-1] > 80):
        position.set_target_volume(-3)  # 开空3手

    # 止损逻辑（slice1提到风险控制）
    if api.get_account().risk_ratio > 0.8:
        position.set_target_volume(0)
        print("触发风控，强制平仓！")
