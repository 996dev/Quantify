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


class MacdStatus(Enum):
    """
    UPWARD：上涨
    FELL：下跌
    EQUAL：相等
    """
    UPWARD = 1
    FELL = 2
    EQUAL = 3


def macd_status(macd_data) -> MacdStatus:
    """
    在判断 MACD 交叉时，通常需要关注以下几个关键点：
    MACD 的组成：
        DIFF 线：短期 EMA（通常为 12 日）与长期 EMA（通常为 26 日）的差值。
        DEA 线：DIFF 线的平滑线（通常为 9 日 EMA）。
        MACD 柱：DIFF 与 DEA 的差值。
    交叉类型：
        金叉（底部交叉）：DIFF 线从下向上穿越 DEA 线，通常视为买入信号。
        死叉（顶部交叉）：DIFF 线从上向下穿越 DEA 线，通常视为卖出信号。
    判断逻辑：
        通过比较当前 K 线的 DIFF 和 DEA 值与前一 K 线的 DIFF 和 DEA 值，可以判断是否发生交叉。
    例如：
        金叉条件：当前DIFF > 当前DEA 且 前一根DIFF <= 前一根DEA。
        死叉条件：当前DIFF < 当前DEA 且 前一根DIFF >= 前一根DEA。
    :param macd_data:
    :return:
    """
    current_diff = macd_data['diff'].iloc[-1]
    current_dea = macd_data['dea'].iloc[-1]
    prev_diff = macd_data['diff'].iloc[-2]
    prev_dea = macd_data['dea'].iloc[-2]

    # 金叉判断
    if current_diff > current_dea and prev_diff <= prev_dea:
        return "金叉（买入信号）"
    # 死叉判断
    elif current_diff < current_dea and prev_diff >= prev_dea:
        return "死叉（卖出信号）"
    else:
        return "无交叉"
