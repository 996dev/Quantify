from datetime import datetime, date

from tqsdk import TqApi, TqAuth, TqSim, TqAccount, TqKq, TqBacktest
from datetime import date
import datetime
from tool.config_watcher import cfg

# 初始化天勤API
auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)

if cfg.real_open:  # 实盘
    api = TqApi(TqAccount(cfg.tq_account_broker_id, cfg.tq_account_account_id, cfg.tq_account_password), auth=auth)
elif cfg.tq_kq:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)
elif cfg.tq_back_test:  # 策略回测
    now = datetime.datetime.now()
    api = TqApi(backtest=TqBacktest(start_dt=date(2025, 2, 20), end_dt=date(now.year, now.month, now.day)), web_gui=True, auth=auth)
else:  # 快期模拟
    api = TqApi(TqKq(), auth=auth)

# 设置合约代码（以螺纹钢为例）
symbol = "SHFE.rb2505"

# 获取日线K线数据
daily_klines = api.get_kline_serial(symbol, duration_seconds=24 * 60 * 60)  # 日线K线

# 获取最新价格和日线开盘价
current_price = daily_klines.close.iloc[-1]  # 最新价格
daily_open_price = daily_klines.open.iloc[-1]  # 日线开盘价

# 获取持仓信息
position = api.get_position(symbol)

if __name__ == '__main__':

    while True:
        # 判断开多单或开空单
        if current_price > daily_open_price:
            print("最新价格大于日线开盘价，准备开多单")
            # 检查是否有空单持仓
            if position.pos_short > 0:
                print("当前有空单持仓，先平空单")
                # 平空单
                close_order = api.insert_order(symbol, direction="BUY", offset="CLOSE", volume=position.pos_short)
                print(f"已下单平空，数量：{position.pos_short}手")

                # 等待平空单成交
                while close_order.status != "FINISHED":
                    api.wait_update()
                print("平空单已成交")

            # 开多单
            print("执行开多单操作")
            open_order = api.insert_order(symbol, direction="BUY", offset="OPEN", volume=1)  # 开1手多单
            print("已下单开多")

            # 等待开多单成交
            while open_order.status != "FINISHED":
                api.wait_update()
            print("开多单已成交")

        elif current_price < daily_open_price:
            print("最新价格小于日线开盘价，准备开空单")
            # 检查是否有多单持仓
            if position.pos_long > 0:
                print("当前有多单持仓，先平多单")
                # 平多单
                close_order = api.insert_order(symbol, direction="SELL", offset="CLOSE", volume=position.pos_long)
                print(f"已下单平多，数量：{position.pos_long}手")

                # 等待平多单成交
                while close_order.status != "FINISHED":
                    api.wait_update()
                print("平多单已成交")

            # 开空单
            print("执行开空单操作")
            open_order = api.insert_order(symbol, direction="SELL", offset="OPEN", volume=1)  # 开1手空单
            print("已下单开空")

            # 等待开空单成交
            while open_order.status != "FINISHED":
                api.wait_update()
            print("开空单已成交")

        else:
            print("最新价格等于日线开盘价，不执行操作")

        # 关闭API
        # api.close()
