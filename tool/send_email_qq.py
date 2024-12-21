import base64
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

from tool.config_watcher import cfg

email = True  # 是否开启邮箱提示，默认为True开启，False为关闭
email_host = cfg.email_qq_host  # QQ邮箱的host地址，不需要修改
email_user = cfg.email_qq_user  # 邮箱地址
email_pass = cfg.password  # 口令/授权码
receivers = [cfg.receivers_qq]  # 接收邮箱
message_from = '量化交易信号提示'  # 发件人名称
message_to = 'FQ'  # 收件人名称
message_subject = '交易信号提示'  # 邮件的主题

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sqq():
    # QQ 邮箱 SMTP 服务器地址
    smtp_server = 'smtp.qq.com'
    smtp_port = 465  # SSL 端口号

    # 发件人和收件人邮箱
    sender = '1023766685@qq.com'
    receiver = '18257125011@163.com'

    # QQ 邮箱 SMTP 授权码
    password = email_pass

    # 邮件内容
    subject = 'Hello, this is a test email'
    content = 'This is a test email sent from Python.'

    # 创建 MIMEText 对象
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header(sender)
    msg['To'] = Header(receiver)
    msg['Subject'] = Header(subject)

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)  # 链接服务器
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        server.quit()


import email.utils
import smtplib
from email.mime.text import MIMEText  # 发送文本
from email.mime.image import MIMEImage  # 发送图片
from email.mime.multipart import MIMEMultipart
from email.header import Header

"""
POP3/SMTP 设置方法
用户名/帐户： 你的QQ邮箱完整的地址
密码： 生成的授权码
电子邮件地址： 你的QQ邮箱的完整邮件地址
接收邮件服务器： pop.qq.com，使用SSL，端口号995
发送邮件服务器： smtp.qq.com，使用SSL，端口号465或587
"""
# smtp.qq.com，使用SSL，端口号465或587
# 授权码：lpquuutuiiuncaih

email_addr_send = cfg.email_qq_user  # 发送者邮箱地址
email_addr_recv = cfg.receivers_qq  # 接收者邮箱地址
email_pass = cfg.password  # 授权码

# smtp邮箱服务器
smtp_server = cfg.email_qq_host


# 发送文本
def send_text():
    # MIMEText三个主要参数
    # 1. 邮件内容
    # 2. MIME子类型，plain表示text类型
    # 3. 邮件编码格式，使用"utf-8"避免乱码
    msg = MIMEText('恭喜，您在12306抢票成功，请及时支付！', 'plain', 'utf-8')  # 邮件内容

    # 发件人
    # msg['From'] = formataddr([发件人, 发件人邮箱地址])
    # msg['From'] = email_addr    #发送者的邮箱地址
    msg['From'] = email.utils.formataddr(("输入发送者的姓名", email_addr_send))

    # 收件人：可以有多个、写成一个列表
    # [xxx@qq.com, 111@qq.com]
    # msg['To'] = email.utils.formataddr(("输入接收者的姓名", email_addr_recv))
    msg['To'] = email_addr_recv  # 接收者的邮箱地址

    # 邮件标题
    # msg['Subject'] = "Hehuyi Test"
    subject = '恭喜您，Python已为您在12306抢票成功，请及时支付！ '
    msg['Subject'] = Header(subject, 'utf-8')

    # 实例化stmp对象
    # 由于安全问题，通常不直接使用smtplib.SMTP来实例化，第三方邮箱会认为它是不安全的而报错
    # 使用加密过的SMTP_SSL来实例化
    stmp_object = smtplib.SMTP_SSL(smtp_server)

    # 链接stmp服务器
    # SMTP.connect(host,port)：连接远程smtp主机
    stmp_object.connect(smtp_server, 465)  # 链接服务器

    # 登录stmp服务器
    # SMTP.login(user, password)：远程smtp主机的校验方法
    stmp_object.login(email_addr_send, email_pass)  # 登录邮箱地址

    # 向其他人发送邮箱内容
    # SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options])：实现邮件的发送功能
    # stmp_object.sendmail（发件人、收件人（列表）、邮件内容）
    stmp_object.sendmail(email_addr_send, email_addr_recv.split(','), msg.as_string())  # 向邮箱发送消息

    print('邮件发送成功！')
    stmp_object.quit()


# 发送图片
def send_img():
    msg = MIMEMultipart()
    msg['From'] = email.utils.formataddr(('我', email_addr_send))
    msg['To'] = email.utils.formataddr(("你", email_addr_recv))
    msg['Subject'] = "邮件标题：发送图片"

    with open('2.png', 'rb') as f:
        img = f.read()
    msg_img = MIMEImage(img)

    msg.attach(msg_img)

    # 连接stmp服务
    stmp_svc = smtplib.SMTP_SSL(smtp_server)
    stmp_svc.connect(smtp_server, 465)
    stmp_svc.login(email_addr_send, email_pass)
    stmp_svc.set_debuglevel(True)

    try:
        stmp_svc.sendmail(email_addr_send, email_addr_recv, msg=msg.as_string())
    except Exception as e:
        print(e)


def send_email(email_message):
    """
    发送邮件提示信息
    :param email_message:邮件内容

    :param email_from:发件人名称
    :param email_to:收件人名称
    :param email_subject:邮件主题
    :param email_host:SMTP 服务器主机,qq邮箱为："smtp.qq.com"
    :param email_user: 邮箱发送人地址
    :param email_pass: 邮箱SMTP授权码
    :param email_receivers:邮箱接收人地址
    """
    if email:
        message = MIMEText(email_message, 'plain', 'utf-8')
        message['From'] = Header(message_from)
        message['To'] = Header(message_to, 'utf-8')
        message['Subject'] = Header(message_subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(host=email_host)
            smtpObj.connect(email_host, 465)  # 465为SMTP加密端口号
            smtpObj.login(email_user, email_pass)
            smtpObj.sendmail(email_user, receivers, message.as_string())
            print('邮件发送成功：{}'.format(email_message))
        except Exception as e:
            print(e)
            print('发送邮件失败')
    else:
        print(email_message)


# def send_qq_mail():
#     sender = user = email_user
#     passwd = email_pass
#
#     # 写成数组，将发给这三者
#     receiver = [receivers]
#
#     msg = MIMEText(f'Python 邮件发送测试 {time.time()}', 'plain', 'utf-8')
#     msg['From'] = f'=?UTF-8?B?{base64.b64encode("好".encode()).decode()}?= <sender@qq.com>'
#     msg['To'] = 'you'  # 每个人都会看到这个内容
#     msg['Subject'] = 'Python SMTP 邮件测试'  # 点开详情后的标题
#
#     try:
#         # 建立 SMTP 、SSL 的连接
#         smtp = smtplib.SMTP_SSL(email_host, 465)
#         # 登录
#         smtp.login(user, passwd)
#         # 发送邮件 发送方，接收方，发送的内容
#         smtp.sendmail(sender, receiver, msg.as_string())
#         print('邮件发送成功')
#         smtp.quit()
#     except Exception as e:
#         print(e)
#         print('发送邮件失败')

def send_email():
    message = MIMEText("content")
    message['To'] = email.utils.formataddr(('收件人姓名', cfg.receivers_qq))
    message['From'] = email.utils.formataddr(('发送人姓名', email_user))
    message['Subject'] = '文件内容'

    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(email_user, email_pass)

    try:
        server.sendmail(email_user, [cfg.receivers_qq], msg=message.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    message = '成功开仓 SHFE.au2408'
    # send_email(message)
    # send_email()
    # sqq()
