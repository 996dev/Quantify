# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from tqsdk import TqApi, TqAuth, TargetPosTask
from qlib.data import D
from qlib.contrib.model.gbdt import LGBModel
from qlib.workflow import R
from qlib.utils import init_instance_by_config

# ====================
# 配置部分
# ====================
SYMBOL = "SHFE.rb2409"  # 螺纹钢主力合约
QLIB_CONFIG = {
    "model": {
        "class": "LGBModel",
        "module_path": "qlib.contrib.model.gbdt",
        "kwargs": {
            "loss": "mse",
            "colsample_bytree": 0.8,
            "subsample": 0.8,
            "eta": 0.05,
            "seed": 42
        }
    }
}


# ====================
# 数据桥接模块
# ====================
class TqsdkDataBridge:
    def __init__(self, api, symbol, freq=900):
        self.api = api
        self.klines = api.get_kline_serial(symbol, freq, 200)

    def get_qlib_features(self):
        """将tqsdk数据转换为Qlib特征"""
        df = pd.DataFrame({
            "$open": self.klines.open,
            "$high": self.klines.high,
            "$low": self.klines.low,
            "$close": self.klines.close,
            "$volume": self.klines.volume,
            "datetime": pd.to_datetime(self.klines.datetime, unit='ns')
        }).set_index("datetime")

        # 添加技术指标
        df["MA5"] = df["$close"].rolling(5).mean()
        df["MA10"] = df["$close"].rolling(10).mean()
        df["RSI"] = self._calc_rsi(df["$close"], 14)
        return df.dropna()

    def _calc_rsi(self, series, window):
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))


# ====================
# 策略引擎
# ====================
class HybridStrategy:
    def __init__(self, api, symbol):
        self.api = api
        self.symbol = symbol
        self.data_bridge = TqsdkDataBridge(api, symbol)
        self.position = TargetPosTask(api, symbol)
        self.model = self._init_model()

    def _init_model(self):
        """初始化Qlib模型"""
        model = init_instance_by_config(QLIB_CONFIG["model"])
        if R.list_models():
            model = R.load_model(R.list_models()[-1])  # 加载最新模型
        return model

    def generate_signal(self, features):
        """生成交易信号"""
        # 创建Qlib数据格式
        data_handler = D.features(features, ["$close", "MA5", "MA10", "RSI"])

        # 获取预测结果
        pred = self.model.predict(data_handler)
        return pred.iloc[-1]  # 返回最新预测值

    def execute_trade(self, signal):
        """执行交易逻辑"""
        if signal > 0.7:
            self.position.set_target_volume(3)  # 做多
        elif signal < 0.3:
            self.position.set_target_volume(-3)  # 做空
        else:
            self.position.set_target_volume(0)  # 平仓


# ====================
# 主运行流程
# ====================
def main():
    api = TqApi(auth=TqAuth("your_account", "your_password"))
    strategy = HybridStrategy(api, SYMBOL)

    try:
        while True:
            api.wait_update()

            if api.is_changing(strategy.data_bridge.klines):
                # 获取最新数据
                features = strategy.data_bridge.get_qlib_features()

                # 生成信号
                signal = strategy.generate_signal(features)
                print(f"[Signal] {pd.Timestamp.now()}: {signal:.2f}")

                # 执行交易
                strategy.execute_trade(signal)

    finally:
        api.close()



# 在HybridStrategy类中添加以下方法
def online_retrain(self, new_data):
    """在线增量训练"""
    updated_data = D.features(
        pd.concat([self.data_bridge.get_qlib_features(), new_data]),
        ["$close", "MA5", "MA10", "RSI"]
    )
    self.model.fit(updated_data)
    R.save_model(self.model, prefix="online_")  # 保存增量模型

def risk_management(self):
    """实时风控检查"""
    account = self.api.get_account()
    if account.risk_ratio > 0.9:
        self.position.set_target_volume(0)
        print("触发风险控制，强制平仓！")

# 1.初始化Qlib数据（示例）
# python -m qlib run_all --cache_dir ~/.qlib/qlib_cache/cn_data --region cn
# 2.离线训练脚本示例
# from qlib.contrib.data.handler import Alpha158
#
# dataset = Alpha158().get_data()
# model = LGBModel(**QLIB_CONFIG["model"]["kwargs"])
# model.fit(dataset)
# R.save_model(model, "base_model")

# 3.在策略循环中添加
# print(f"当前账户状态：\n"
#       f"净值：{api.get_account().balance}\n"
#       f"持仓：{api.get_position(SYMBOL).pos}\n"
#       f"风险率：{api.get_account().risk_ratio:.2%}")
if __name__ == "__main__":
    main()
