import os
from jinja2 import Environment, FileSystemLoader

# 获取模板
env = Environment(loader=FileSystemLoader("./"))
template = env.get_template("jinjia2_strategy.j2")

# 删除已有的生成文件
# for f in os.listdir("./output"):
#     path_file = os.path.join("./output", f)
#     if os.path.isfile(path_file):
#         os.remove(path_file)

大商所 = ['DCE.jm2509', 'DCE.bb2511', 'DCE.m2509', 'DCE.c2507', 'DCE.jd2506', 'DCE.eb2506', 'DCE.i2509', 'DCE.b2509',
          'DCE.p2509', 'DCE.j2509', 'DCE.a2507', 'DCE.cs2507',
          'DCE.v2509', 'DCE.lh2509', 'DCE.lg2507', 'DCE.fb2506', 'DCE.pg2506', 'DCE.l2509', 'DCE.y2509', 'DCE.rr2507',
          'DCE.pp2509', 'DCE.eg2509']
上期所 = ['SHFE.al2507', 'SHFE.ao2509', 'SHFE.ss2507', 'SHFE.pb2506', 'SHFE.fu2507', 'SHFE.ru2509', 'SHFE.bu2506',
          'SHFE.zn2506', 'SHFE.wr2510', 'SHFE.cu2506',
          'SHFE.sp2507', 'SHFE.hc2510', 'SHFE.rb2510', 'SHFE.br2506', 'SHFE.ag2508', 'SHFE.sn2506', 'SHFE.ni2506',
          'SHFE.au2508']
郑商所 = ['CZCE.RM509', 'CZCE.OI509', 'CZCE.JR509', 'CZCE.SM509', 'CZCE.UR509', 'CZCE.CJ509', 'CZCE.TA509',
          'CZCE.CY507', 'CZCE.AP510', 'CZCE.WH509', 'CZCE.LR509',
          'CZCE.SA509', 'CZCE.RS507', 'CZCE.SH509', 'CZCE.MA509', 'CZCE.FG509', 'CZCE.CF509', 'CZCE.PM509',
          'CZCE.RI509', 'CZCE.PR507', 'CZCE.SR509', 'CZCE.SF507',
          'CZCE.PK510', 'CZCE.PF507', 'CZCE.ZC509', 'CZCE.PX509']
能源交易所 = ['INE.ec2506', 'INE.nr2506', 'INE.lu2507', 'INE.bc2506', 'INE.sc2506']
广州期货交易所 = ['GFEX.lc2507', 'GFEX.si2506', 'GFEX.ps2506']
# 生成新的文件
for i in 广州期货交易所:
    data = {
        "class_name": "User",
        "symbol_name": i,
        "args": ["name", "age"],
        "methods": [
            {
                "name": "greet",
                "args": ["greeting"],
                "doc": "生成问候语",
                "return_type": "str",
                "default_return": "f'{greeting}, {self.name}'"
            },
            {
                "name": "is_adult",
                "doc": "是否成年",
                "return_type": "bool",
                "default_return": "self.age >= 18"
            }
        ]
    }
    output = template.render(data)
    if not os.path.exists('./output'):
        os.mkdir('./output')
    with open("./output/%s.py" % i, 'w', encoding='utf-8') as out:
        out.write(output)
