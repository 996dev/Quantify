from tqsdk import TqApi, TqAuth, TqSim, TargetPosTask
import pandas as pd

api = TqApi(TqSim(), auth=TqAuth("用户名", "密码"))
klines = api.get_kline_serial("SHFE.rb2409", 900, 2000)  # 螺纹钢主力合约

# 均线计算（参考slice1的ma实现）
klines["ma5"] = klines.close.rolling(5).mean()  # 5日均线
klines["ma10"] = klines.close.rolling(10).mean()  # 10日均线
klines["ma20"] = klines.close.rolling(20).mean()  # 20日均线

position = TargetPosTask(api, "SHFE.rb2409")  # 持仓管理

while True:
    api.wait_update()

    # 最新三根K线数据（slice3提到的iloc用法）
    current = klines.iloc[-1]
    prev1 = klines.iloc[-2]
    prev2 = klines.iloc[-3]

    # 多空信号判断（slice2的均线排列逻辑）
    # 多头条件：5>10>20 且 5日线连续3日上升
    long_cond = (current.ma5 > current.ma10) and (current.ma10 > current.ma20) \
                and (current.ma5 > prev1.ma5) and (prev1.ma5 > prev2.ma5)

    # 空头条件：5<10<20 且 5日线连续3日下降
    short_cond = (current.ma5 < current.ma10) and (current.ma10 < current.ma20) \
                 and (current.ma5 < prev1.ma5) and (prev1.ma5 < prev2.ma5)

    # 交易执行（参考slice3的仓位管理）
    if long_cond:
        position.set_target_volume(3)  # 做多3手
    elif short_cond:
        position.set_target_volume(-3)  # 做空3手
    else:
        position.set_target_volume(0)  # 平仓

    # 风控模块（slice1提到的风险控制）
    if api.get_account().risk_ratio > 0.8:
        position.set_target_volume(0)
        print("触发风险控制，强制平仓！")
        break
