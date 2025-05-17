#! /usr/bin/env python
# coding=utf-8
import os
from string import Template

#
# 代码生成器所需的数据配置字典
# 在需要生成地方使用 ${key-name} 配置，如下：
# class C${Class_Name}
#
config_dict = {
    'CLASSNAME': 'DEFAULT',
    'Class_Name': 'Default',
    'En_name': 'mystruct',
    'Type': 'int',
    'Name': 'value'
}


def gen(tmpl, out):
    if not os.path.exists(out):  # 如不存在目标目录则创建
        os.makedirs(out)
    files = os.listdir(tmpl)  # 获取文件夹中文件和目录列表
    for f in files:
        if os.path.isdir(tmpl + '/' + f):  # 判断是否是文件夹
            gen(tmpl + '/' + f, out + '/' + f)  # 递归调用本函数
        else:
            gen_one_file(tmpl + '/' + f, get_out_filename(f, out), config_dict)  # 拷贝文件


def gen_one_file(tmpl, target, config_dict):
    filePath = target
    class_file = open(filePath, 'w')

    mycode = []

    # 加载模板文件
    template_file = open(tmpl, 'r')
    tmpl = Template(template_file.read())

    # 模板替换
    mycode.append(tmpl.substitute(config_dict))

    # 将代码写入文件
    class_file.writelines(mycode)
    class_file.close()

    print('ok')


def get_out_filename(temp_name, out_dir):
    # 生成文件跟模板名相同
    return out_dir + '/' + temp_name


if __name__ == '__main__':
    gen("templ", "out")
