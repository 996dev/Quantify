import time
from datetime import datetime

from tqsdk.objs import Quote


def now_time(quote: Quote) -> datetime:
    """根据交易所返回的时间，转换成datetime"""
    return datetime.strptime(quote.datetime, "%Y-%m-%d %H:%M:%S.%f")


def local_time() -> datetime:
    """本地时间转换成datetime"""
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return datetime.strptime(localtime, "%Y-%m-%d %H:%M:%S")
