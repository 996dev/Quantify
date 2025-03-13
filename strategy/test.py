from datetime import date

import datetime
from tool.direction import Direction, Offset

if __name__ == '__main__':
    print(f"year:{date.year} month:{date.month} day:{date.day}")

    # 获取当前日期和时间
    now = datetime.datetime.now()

    # 获取年、月、日
    year = now.year
    month = now.month
    day = now.day

    print(year, month, day)

    print(Offset.OPEN.value)

    print(Offset.CLOSE.value)
