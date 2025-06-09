# 数据桥接模块（需处理时区对齐）
import asyncio

from qlib.data import D
from tqsdk import TqApi, TqAuth, TargetPosTask
import pandas as pd

from tool.config_watcher import cfg


# 启用tqsdk高性能模式
# api = TqApi(auth=TqAuth("id","pwd"), _stock=True, _use_gzip=True)
# Qlib缓存加速
# qlib.init(redis_port=6379, redis_host='127.0.0.1')  # 启用Redis缓存

class QlibTqsdkBridge:
    def __init__(self, symbol):
        auth = TqAuth(cfg.tq_auth_user_name, cfg.tq_auth_password)
        self.api = TqApi(auth=auth)
        self.klines = self.api.get_kline_serial(symbol, 900, 200)

    def realtime_to_qlib(self):
        """实时数据格式转换（关键字段映射）"""
        df = self.klines.copy().rename(columns={
            "datetime": "date",
            "open": "$open",
            "high": "$high",
            "low": "$low",
            "close": "$close",
            "volume": "$volume"
        })
        df["date"] = pd.to_datetime(df["date"], unit='ns').dt.tz_localize('Asia/Shanghai')
        return df.set_index("date")


# Qlib模型预测模块（支持在线学习）
from qlib.contrib.model.gbdt import LGBModel
from qlib.workflow import R


class HybridModel:
    def __init__(self):
        self.online_model = LGBModel()
        self.init_offline_model()

    def init_offline_model(self):
        """加载预训练模型"""
        self.offline_model = R.load_model("pretrained_lgb")

    async def online_update(self, new_data):
        """增量训练接口"""
        await self.online_model.fit(new_data)


# 交易执行引擎（带风控检查）
class EnhancedTrader:
    def __init__(self, symbol):
        self.target_pos = TargetPosTask(self.api, symbol)
        self.position = 0

    def execute_with_riskcheck(self, signal):
        """带风控的交易执行"""
        if signal > 0.8 and self.position < 3:
            self.target_pos.set_target_volume(3)
            self.position = 3
        elif signal < 0.2 and self.position > -3:
            self.target_pos.set_target_volume(-3)
            self.position = -3


# 主运行流程（异步架构）
async def hybrid_strategy():
    bridge = QlibTqsdkBridge("SHFE.rb2509")
    model = HybridModel()
    trader = EnhancedTrader("SHFE.rb2509")

    while True:
        # 获取最新数据
        qlib_data = bridge.realtime_to_qlib()

        # 双模型预测
        offline_signal = model.offline_model.predict(qlib_data).iloc[-1]
        online_signal = model.online_model.predict(qlib_data[-50:]).iloc[-1]

        # 信号融合
        final_signal = 0.6 * offline_signal + 0.4 * online_signal

        # 执行交易
        trader.execute_with_riskcheck(final_signal)

        # 增量更新
        await model.online_update(qlib_data[-10:])

        await asyncio.sleep(0.1)  # 控制循环频率

if __name__ == '__main__':
    hybrid_strategy()
