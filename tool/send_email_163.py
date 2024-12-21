import smtplib
from email.mime.text import MIMEText
from email.header import Header

from tool.config_watcher import cfg

# 第三方 SMTP 服务
mail_host = cfg.email_163_host  # 设置服务器
mail_user = cfg.email_163_user  # 用户名
mail_pass = cfg.email_163_pass  # 口令

sender = cfg.sender_163

  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# receivers = ['overwatch@126.com', '994514046@qq.com', '619123443@qq.com', '1903732138@qq.com', '931013465@qq.com',
#              '751821309@qq.com', '783199599@qq.com', '438726534@qq.com', '1040148238@qq.com', '1752722411@qq.com',
#              '330661156@qq.com']
receivers = ['overwatch@126.com', '15350017210@163.com', 'bobdong0912@gmail.com']


# def send():
#     message = MIMEText('量化交易信号 邮件发送测试...', 'plain', 'utf-8')
#     message['From'] = Header("量化交易信号提示", 'utf-8')
#     message['To'] = Header("测试", 'utf-8')
#
#     subject = '量化交易信号 平仓完毕'
#     message['Subject'] = Header(subject, 'utf-8')
#
#     try:
#         smtp = smtplib.SMTP()
#         smtp.connect(mail_host, 25)  # 25 为 SMTP 端口号
#         smtp.login(mail_user, mail_pass)
#         smtp.sendmail(sender, receivers, message.as_string())
#         print("邮件发送成功")
#
#     except smtplib.SMTPException:
#         print("Error: 无法发送邮件")


class Email163:
    def send_message(self, content):
        message = MIMEText('量化交易信号提示 -> ' + content, 'plain', 'utf-8')
        message['From'] = Header("量化交易信号提示", 'utf-8')
        message['To'] = Header("量化交易信号提示", 'utf-8')

        subject = '量化交易信号提示'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtp = smtplib.SMTP()
            smtp.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtp.login(mail_user, mail_pass)
            smtp.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")

        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


email_163 = Email163()

if __name__ == '__main__':
    sebd = ["合约$$$ 开多单", "合约$$$ 开多单", "合约$$$ 开多单", "合约$$$ 开多单", "合约$$$ 开多单"]

    email_163.send_message(sebd.__str__())
