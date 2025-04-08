from tqsdk import TqApi, TqAuth, TqSim
from tqsdk.ta import MACD, KDJ

# 初始化天勤API
api = TqApi(auth=TqAuth("你的账号", "你的密码"))
symbol = "SHFE.rb2401"  # 以螺纹钢2401合约为例
klines = api.get_kline_serial(symbol, duration_seconds=24 * 60 * 60)  # 日线数据

while True:
    api.wait_update()
    if api.is_changing(klines):
        # 计算MACD指标
        macd = MACD(klines, short_period=12, long_period=26, mid_period=9)
        # 计算KDJ指标
        kdj = KDJ(klines, n=9, m1=3, m2=3)

        # 判断条件
        macd_cross = macd["diff"].iloc[-2] < macd["dea"].iloc[-2] and macd["diff"].iloc[-1] > macd["dea"].iloc[-1]  # MACD底部交叉
        kdj_cross = kdj["K"].iloc[-2] < kdj["D"].iloc[-2] and kdj["K"].iloc[-1] > kdj["D"].iloc[-1]  # KDJ底部交叉
        daily_up = klines.close.iloc[-1] > klines.close.iloc[-2]  # 日线上涨

        if macd_cross and kdj_cross and daily_up:
            print("满足条件，执行做多操作")
            # 获取账户信息
            account = api.get_account()
            # 开仓做多
            order = api.insert_order(symbol=symbol, direction="BUY", offset="OPEN", volume=1)
            print("已开仓做多")
            break  # 仅示例，实际策略可能需要更复杂的逻辑

# 关闭API
api.close()
