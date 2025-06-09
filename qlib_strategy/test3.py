from qlib.data import D
from tqsdk import TqApi


class TqDataAdapter:
    def __init__(self, symbol):
        self.api = TqApi()
        self.klines = self.api.get_kline_serial(symbol, 900)

    def to_qlib_format(self):
        return self.klines.rename(columns={
            "datetime": "date",
            "open": "$open",
            "high": "$high",
            "low": "$low",
            "close": "$close"
        }).set_index("date")

# 1.数据对齐：确保 tqsdk 的时区设置与 qlib.init () 一致
# qlib.init(region="cn", tz="Asia/Shanghai")

# 2.特征工程：扩展 Qlib 原生特征集
# from qlib.contrib.data.handler import Alpha158
#
#
# class EnhancedHandler(Alpha158):
#     def __init__(self, instruments="rb2409", **kwargs):
#         super().__init__(instruments=instruments, **kwargs)
#         self._add_tqsdk_features()
#
#     def _add_tqsdk_features(self):
#         self.features += ["MA5", "MA10", "RSI"]

# 3.模型部署：使用 QLib 的模型服务化功能
# from qlib.workflow import R
# from qlib.serving import QlibServer
#
# # 保存训练好的模型
# R.save_model(lgb_model, "tq_lgb_v1")
#
# # 启动预测服务
# QlibServer.start(port=8989)
