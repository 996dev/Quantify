import sqlite3
import time
connect = sqlite3.connect('test.db')
cur = connect.cursor()
if __name__ == '__main__':
    # 徽商期货 账号 密码
    # 天勤量化 账号 密码
    # 回测 模拟 实盘
    start = time.time()
    for i in range(3):
        cur.execute(
            """INSERT INTO user(futures_account, futures_password,tq_account,tq_password,account_type,disable) VALUES('18257125011','123456','996dev','123456',1,0);""")
        connect.commit()

    end = time.time()
    print('程序运行时间为: %s Seconds' % (end - start))
