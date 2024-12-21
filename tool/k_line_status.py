from enum import Enum


class KLineStatus(Enum):
    """
    UPWARD：上涨
    FELL：下跌
    EQUAL：相等
    """
    UPWARD = 1
    FELL = 2
    EQUAL = 3


def k_line_status(close, open) -> KLineStatus:
    """
    判断上涨还是下跌

    上涨：收盘价高于开盘价 close>open 多开 空平
    下跌：收盘价低于开盘价 close<open 空开 多平
    等于：收盘价等于开盘价 close=open 使用上一个的状态
     pandas.DataFrame: 本函数总是返回一个 pandas.DataFrame 实例. 行数=data_length, 包含以下列:
    """

    if close > open:
        return KLineStatus.UPWARD
    if close < open:
        return KLineStatus.FELL
    if close == open:
        return KLineStatus.EQUAL


"""
   日线，30分钟线。
   日线 红了；30分钟线红了；做多；如果有持仓标的，则不再开仓；风险把控->todo 1:如果在上涨的趋势中下降过多，则需要处理？
   日线 绿了；30分钟线绿了；做空；如果有持仓标的，则不在开仓；风险把控->todo 1:如果在下降的趋势中上涨过多，则需要处理？

   如何使用代码表示？？ -> 日线红了 30分钟线红了，开仓做多。
   如何使用代码表示？？ -> 日线绿了 30分钟线绿了，开仓做空。

   * id: 1234 (k线序列号)
   * datetime: 1501080715000000000 (K线起点时间(按北京时间)，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数)
   * open: 51450.0 (K线起始时刻的最新价)
   * high: 51450.0 (K线时间范围内的最高价)
   * low: 51450.0 (K线时间范围内的最低价)
   * close: 51450.0 (K线结束时刻的最新价)
   * volume: 11 (K线时间范围内的成交量)
   * open_oi: 27354 (K线起始时刻的持仓量)
   * close_oi: 27355 (K线结束时刻的持仓量)

   """
