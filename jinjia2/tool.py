import os
from jinja2 import Environment, FileSystemLoader

#获取模板
env = Environment(loader = FileSystemLoader(searchpath=""))
template = env.get_template("dag_template")




#删除已有的生成文件
for f in os.listdir("./output"):
    path_file = os.path.join("./output", f)
    if os.path.isfile(path_file):
        os.remove(path_file)

#生成新的文件
for i in range(1, 10):
    output = template.render({'dag_name' : "benchmark%d" % i})
    with open("./output/bm%d.py" % i, 'w') as out:
        out.write(output)
