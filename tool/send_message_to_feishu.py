import requests
import json

from tool.config_watcher import cfg

## 替换为你的自定义机器人的 webhook 地址。
url = cfg.feishu_webhook_url
## 将消息卡片内容粘贴至此处。
card_json = r'''
{
  "config": {
    "wide_screen_mode": true
  },
  "elements": [
    {
      "alt": {
        "content": "",
        "tag": "plain_text"
      },
      "img_key": "img_v2_bfd72a81-1533-4699-995d-12a675708d0g",
      "tag": "img"
    },
    {
      "tag": "div",
      "text": {
        "content": "你是否曾因为一本书而产生心灵共振，开始感悟人生？\n你有哪些想极力推荐给他人的珍藏好书？\n\n加入 **4·23 飞书读书节**，分享你的**挚爱书单**及**读书笔记**，**赢取千元读书礼**！\n\n📬 填写问卷，晒出你的珍藏好书\n😍 想知道其他人都推荐了哪些好书？马上[入群围观](https://open.feishu.cn/)\n📝 用[读书笔记模板](https://open.feishu.cn/)（桌面端打开），记录你的心得体会\n🙌 更有惊喜特邀嘉宾 4月12日起带你共读",
        "tag": "lark_md"
      }
    },
    {
      "actions": [
        {
          "tag": "button",
          "text": {
            "content": "立即推荐好书",
            "tag": "plain_text"
          },
          "type": "primary",
          "url": "https://open.feishu.cn/"
        },
        {
          "tag": "button",
          "text": {
            "content": "查看活动指南",
            "tag": "plain_text"
          },
          "type": "default",
          "url": "https://open.feishu.cn/"
        }
      ],
      "tag": "action"
    }
  ],
  "header": {
    "template": "turquoise",
    "title": {
      "content": "📚晒挚爱好书，赢读书礼金",
      "tag": "plain_text"
    }
  }
}
'''

card_json_1 = {
    "msg_type": "text",
    "content": {
        "text": "new update notification"
    }
}

card_json_2 = r'''
{
     "msg_type": "interactive",
     "card": {
         "elements": [{
                 "tag": "div",
                 "text": {
                         "content": "**West Lake**, located at No. 1 Longjing Road, Xihu District, Hangzhou City, Zhejiang Province, west of Hangzhou City, with a total area of 49 square kilometers, a catchment area of 21.22 square kilometers, and a lake area of 6.38 square kilometers km.",
                         "tag": "lark_md"
                 }
         }, {
                 "actions": [{
                         "tag": "button",
                         "text": {
                                 "content": "More attractions introduction: Rose:",
                                 "tag": "lark_md"
                         },
                         "url": "https://www.example.com",
                         "type": "default",
                         "value": {}
                 }],
                 "tag": "action"
         }],
         "header": {
                 "title": {
                         "content": "Today's travel recommendation",
                         "tag": "plain_text"
                 }
         }
     }
}
'''


class Feishu():
    # def __init__(self):
    #     pass

    def send_message(self, content):
        # text_message = {
        #     "msg_type": "text",
        #     "content": {
        #         "text": content
        #     }
        # }
        text_message = {
            "text": content
        }
        body = json.dumps({"msg_type": "text", "content": text_message})
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, data=body, headers=headers)
        print(response.request.body)
        return response.json


fei_shu = Feishu()

if __name__ == '__main__':
    # todo 测试
    # body = json.dumps({"msg_type": "interactive", "card": card_json})
    body = json.dumps({"msg_type": "text", "content": {
        "text": "NI"
    }})
    headers = {"Content-Type": "application/json"}
    res = requests.post(url=url, data=body, headers=headers)
    print(res.request.body)
    print(res.text)
