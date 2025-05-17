import random
import requests
import time
import pandas as pd
import datetime
from wxauto import WeChat

wx = WeChat()


def test(playerNickName, tradeDate, groupType, companyName, sort):
    url = 'https://spdsi.qhrb.com.cn/api/spsread2025/groupBaseFront/getBaseScoreTotalListAdm'
    params = {'internalAccount': '', 'playerNickName': playerNickName, 'tradeDate': tradeDate,
              'deadlineTime': tradeDate, 'groupType': groupType, 'index': 1, 'size': 50, 'selType': 0, 'breedCode': 0}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, params=params)
    # 获取响应内容
    print(response.status_code)  # 状态码
    print(response.text)  # 响应内容
    print(f"排序位置：{sort}")
    if response.status_code == 200:
        data = response.json()
        if data['dataPoints']['total'] > 0:
            res = data['dataPoints']['list']
            if len(res) > 0:
                for i in res:
                    if companyName in i['companyName']:
                        # and i['playerId'] == ""
                        i['编号'] = sort
                        if i['playerNickName'] == '无为' and i['companyName'] == '广发期货':
                            list_result.append(i)
                        else:
                            list_result.append(i)
        else:
            print("无需查找")
            # test(playerNickName, tradeDate, 2)


list_name = ['岳晓辉', '可胜投资', '蜗牛也是牛', '得鹿梦鱼', '半部经书', '云中仙', '陈凯强', '猎二', '蘑菇', '杀庄侠',
             '大道至简', '和鸣', '秋秋一号', '乐斗期', '工画师',
             '郑智元', '一瓢够了', '胜勇', '徐成明', '无为', '抱朴守中', '等待请等待', '谛泽铭']
list_result = []
list_search = [
    {'name': '中场休息中', 'companyName': '东航', 'groupType': 1, 'sort': 1},
    {'name': '蜗牛也是牛', 'companyName': '广州金控期货', 'groupType': 2, 'sort': 2},
    # {'name': '蜗牛也牛', 'companyName': '国信期货', 'groupType': 2, 'sort': 2},
    {'name': '得鹿梦鱼', 'companyName': '宏源', 'groupType': 1, 'sort': 3},
    {'name': '半部经书', 'companyName': '宏源', 'groupType': 1, 'sort': 4},
    {'name': '云中仙', 'companyName': '国元', 'groupType': 2, 'sort': 5},
    {'name': '陈凯强', 'companyName': '山金', 'groupType': 2, 'sort': 6},
    {'name': '猎二', 'companyName': '渤海', 'groupType': 1, 'sort': 7},
    {'name': '岳晓辉', 'companyName': '徽商期货', 'groupType': 1, 'sort': 8},
    {'name': '蘑菇', 'companyName': '光大', 'groupType': 2, 'sort': 9},
    {'name': '杀庄侠', 'companyName': '宝城', 'groupType': 1, 'sort': 10},
    {'name': '大道至简', 'companyName': '宏源', 'groupType': 4, 'sort': 11},
    {'name': '和鸣', 'companyName': '弘业', 'groupType': 1, 'sort': 12},
    {'name': '秋秋一号', 'companyName': '渤海', 'groupType': 1, 'sort': 13},
    {'name': '乐斗期', 'companyName': '中辉', 'groupType': 1, 'sort': 14},
    {'name': '工画师', 'companyName': '新世纪', 'groupType': 2, 'sort': 15},
    {'name': '郑智元', 'companyName': '冠通', 'groupType': 1, 'sort': 16},
    {'name': '一瓢够了', 'companyName': '东吴', 'groupType': 1, 'sort': 17},
    {'name': '胜勇', 'companyName': '华安', 'groupType': 1, 'sort': 18},
    {'name': '徐成明', 'companyName': '宝城', 'groupType': 1, 'sort': 19},
    {'name': '无为', 'companyName': '广发', 'groupType': 1, 'sort': 20},
    {'name': '抱朴守中', 'companyName': '华安', 'groupType': 1, 'sort': 21},
    {'name': '等待请等待', 'companyName': '金信', 'groupType': 1, 'sort': 22},
    {'name': '谛泽铭', 'companyName': '华联', 'groupType': 1, 'sort': 23},
    {'name': '寻找投资方', 'companyName': '安粮', 'groupType': 1, 'sort': 24},
]
if __name__ == '__main__':
    now = datetime.datetime.now()
    tradeDate = now.strftime("%Y-%m-%d")
    print(tradeDate)  # 输出：2021-05-17 15:30:45
    # tradeDate = '2025-05-07'
    for search in list_search:
        try:
            test(search['name'], tradeDate, search['groupType'], search['companyName'], sort=search['sort'])
        except Exception as e:
            print(f"请求 出错: {e}")

        # delay = 3 + random.uniform(-0.5, 0.5)  # 2.5到3.5秒之间的随机延迟
        # time.sleep(delay)
    list_new = []
    for e in list_result:
        n = {}
        n['编号'] = e['编号']
        n['排名'] = e['sortNo']
        n['客户昵称'] = e['playerNickName']
        n['当日市值权益(元)'] = e['dateBalanceToday']
        n['风险度(%)'] = e['riskDegree']
        n['净利润'] = e['netProfit']
        n['净利润得分'] = e['netProfitScore']
        n['回撤率(%)'] = e['withrawalRate']
        n['回撤率得分'] = e['withrawalRateScore']
        n['日净值'] = e['netWorth']
        n['累计净值'] = e['totalNetWorth']
        n['累计净值得分'] = e['netWorthScore']
        n['最大本金收益率(%)'] = e['maxPrincipal']
        n['最大本金收益率得分'] = e['maxPrincipalScore']
        n['综合得分'] = e['comprehensiveScore']
        n['指定交易商'] = e['companyName']
        n['操作指导'] = e['operateGuide']
        n['交易日期'] = e['tradeDate']
        n['组别'] = e['groupType']
        list_new.append(n)
        # 转换为DataFrame并保存
    df = pd.DataFrame(list_new)
    file_name = tradeDate + '-排名信息.xlsx'
    df.to_excel(file_name, index=False)

    files = [
        'C:/Users/Atlantis/Desktop/Quantify/qhds/' + file_name,
    ]
    who = '俱乐部第一届期货大赛(公正客观)'
    wx.SendFiles(filepath=files, who=who)  # 向`文件传输助手`发送上述三个文件
    wx.SendMsg('测试群发送文件', who=who)
