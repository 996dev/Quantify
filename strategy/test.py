from datetime import date

import datetime


if __name__ == '__main__':
    print(f"year:{date.year} month:{date.month} day:{date.day}")

    # 获取当前日期和时间
    now = datetime.datetime.now()

    # 获取年、月、日
    year = now.year
    month = now.month
    day = now.day

    print(year, month, day)
