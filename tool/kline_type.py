from enum import Enum


class Kline(Enum):
    """
    duration_seconds(int): K线数据周期, 以秒为单位。例如: 1
    分钟线为60, 1
    小时线为3600, 日线为86400。 \
            注意: 周期在日线以内时此参数可以任意填写, 在日线以上时只能是日线(86400)
    的整数倍, 最大为28天(86400 * 28)。
    """
    SECONDS1 = 1
    SECONDS5 = 5
    SECONDS10 = 10
    SECONDS15 = 15
    SECONDS30 = 30
    MINUTE1 = 60
    MINUTE3 = 180
    MINUTE5 = 300
    MINUTE10 = 600
    MINUTE15 = 900
    MINUTE30 = 1800
    HOUR1 = 3600
    HOUR2 = 7200
    HOUR4 = 14400
    DAILY = 86400
