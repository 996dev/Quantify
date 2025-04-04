from tqsdk import TqApi, TqAuth, TqSim

# 初始化天勤API
api = TqApi(auth=TqAuth("你的账号", "你的密码"))

# 设置合约代码（以螺纹钢为例）
symbol = "SHFE.rb2305"

# 获取日线K线数据
daily_klines = api.get_kline_serial(symbol, duration_seconds=24 * 60 * 60)  # 日线K线

# 获取最新价格和日线开盘价
current_price = daily_klines.close.iloc[-1]  # 最新价格
daily_open_price = daily_klines.open.iloc[-1]  # 日线开盘价

# 获取持仓信息
position = api.get_position(symbol)

# 止损计数器
stop_loss_count = 0

# 最大止损次数
max_stop_loss_count = 3

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

    # 设置止损逻辑
    stop_loss_price = current_price * 0.99  # 止损价格为当前价格的99%
    print(f"设置止损价格为：{stop_loss_price}")

    # 监控止损
    while True:
        api.wait_update()
        current_price = daily_klines.close.iloc[-1]  # 获取最新价格
        if current_price <= stop_loss_price:
            print("触发止损，平多单")
            # 平多单
            close_order = api.insert_order(symbol, direction="SELL", offset="CLOSE", volume=1)
            print("已下单平多")

            # 等待平多单成交
            while close_order.status != "FINISHED":
                api.wait_update()
            print("平多单已成交")

            # 更新止损计数器
            stop_loss_count += 1
            print(f"当前止损次数：{stop_loss_count}")

            # 检查是否达到最大止损次数
            if stop_loss_count >= max_stop_loss_count:
                print("达到最大止损次数，退出策略")
                break

            # 重新开多单
            print("重新开多单")
            open_order = api.insert_order(symbol, direction="BUY", offset="OPEN", volume=1)
            print("已下单开多")

            # 等待开多单成交
            while open_order.status != "FINISHED":
                api.wait_update()
            print("开多单已成交")

            # 更新止损价格
            stop_loss_price = current_price * 0.99
            print(f"更新止损价格为：{stop_loss_price}")

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

    # 设置止损逻辑
    stop_loss_price = current_price * 1.01  # 止损价格为当前价格的101%
    print(f"设置止损价格为：{stop_loss_price}")

    # 监控止损
    while True:
        api.wait_update()
        current_price = daily_klines.close.iloc[-1]  # 获取最新价格
        if current_price >= stop_loss_price:
            print("触发止损，平空单")
            # 平空单
            close_order = api.insert_order(symbol, direction="BUY", offset="CLOSE", volume=1)
            print("已下单平空")

            # 等待平空单成交
            while close_order.status != "FINISHED":
                api.wait_update()
            print("平空单已成交")

            # 更新止损计数器
            stop_loss_count += 1
            print(f"当前止损次数：{stop_loss_count}")

            # 检查是否达到最大止损次数
            if stop_loss_count >= max_stop_loss_count:
                print("达到最大止损次数，退出策略")
                break

            # 重新开空单
            print("重新开空单")
            open_order = api.insert_order(symbol, direction="SELL", offset="OPEN", volume=1)
            print("已下单开空")

            # 等待开空单成交
            while open_order.status != "FINISHED":
                api.wait_update()
            print("开空单已成交")

            # 更新止损价格
            stop_loss_price = current_price * 1.01
            print(f"更新止损价格为：{stop_loss_price}")

else:
    print("最新价格等于日线开盘价，不执行操作")

# 关闭API
api.close()
