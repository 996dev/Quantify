from tqsdk import TqApi, TqAuth



# 协程示例，为每个合约创建 task
from tqsdk import TqApi, TqAuth


async def demo(SYMBOL):
    quote = await api.get_quote(SYMBOL)  # 支持 await 异步，这里会订阅合约，等到收到合约行情才返回
    print(f"quote: {SYMBOL}", quote.datetime, quote.last_price)  # 这一行就会打印出合约的最新行情
    async with api.register_update_notify() as update_chan:
        async for _ in update_chan:
            if api.is_changing(quote):
                print(SYMBOL, quote.datetime, quote.last_price)



api = TqApi(auth=TqAuth("快期账户", "账户密码"))

symbol_list = ["SHFE.rb2107", "DCE.m2109"]  # 设置合约代码
for symbol in symbol_list:
    api.create_task(demo(symbol))  # 为每个合约创建异步任务

while True:
    api.wait_update()


# 1. 创建合约列表（支持任意数量）
symbols = [
    "SHFE.cu1901",
    "SHFE.cu1902",
    "DCE.m2105",
    "CZCE.MA109"
]

api = TqApi(auth=TqAuth("账号", "密码"))

# 2. 批量订阅行情（支持列表传参）
quotes = api.get_quote(symbols)  # 返回字典结构

# 3. 批量订阅K线（支持多周期）
kline_dict = {
    "5分钟": api.get_kline_serial(symbols, 5*60),
    "1小时": api.get_kline_serial(symbols, 60*60)
}

# 4. 统一处理更新（自动合并数据包）
while True:
    api.wait_update()
    for symbol in symbols:
        if api.is_changing(quotes[symbol]):
            print(f"{symbol} 最新价:{quotes[symbol].last_price}")
