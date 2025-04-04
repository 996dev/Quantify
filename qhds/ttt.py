import pandas as pd

if __name__ == '__main__':
    # 字典列表形式的集合数据
    data = [
        {'姓名': '张三', '年龄': 25, '城市': '北京'},
        {'姓名': '李四', '年龄': 30, '城市': '上海'},
        {'姓名': '王五', '年龄': 28, '城市': '广州'}
    ]

    # 转换为DataFrame并保存
    df = pd.DataFrame(data)
    df.to_excel('output_dict.xlsx', index=False)

    print("Excel文件已生成: output_dict.xlsx")
