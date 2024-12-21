import time
import hmac
import hashlib
import base64
import urllib.parse
import requests, json

from tool.config_watcher import cfg

# 加签
webhook = cfg.dingding_webhook_url  # 钉钉机器人webhook
timestamp = str(round(time.time() * 1000))
secret = cfg.dingding_secret  # 钉钉机器人秘钥
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
# print(string_to_sign)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
# print(timestamp)
# print(sign)
webhook = webhook + '&timestamp=' + timestamp + '&sign=' + sign
# print(webhook)
# 定义数据类型
headers = {'Content-Type': 'application/json'}


class DingDing():
    def send_message(self, content):
        data = {"msgtype": "text", "text": {"content": content}, "isAtAll": True}
        # 发送post请求
        response = requests.post(webhook, data=json.dumps(data), headers=headers)
        print(response.text)
        return response.json


ding_ding = DingDing()

if __name__ == '__main__':
    data = {"msgtype": "text", "text": {"content": '机器人将发送该备注'}, "isAtAll": True}

    # ding_ding.send_message("你好")
    # 发送post请求
    res = requests.post(webhook, data=json.dumps(data), headers=headers)
    print(res.text)
