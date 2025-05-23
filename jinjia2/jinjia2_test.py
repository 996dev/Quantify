import os

from jinja2 import Environment, FileSystemLoader

# env = Environment(
#     loader=FileSystemLoader("./templates"),
#     trim_blocks=True,  # 自动去除模板块的换行
#     lstrip_blocks=True  # 自动去除模板块的左空格
# )
#
# template = env.get_template("./python_class.j2")

env = Environment(loader=FileSystemLoader("./"))
template = env.get_template("python_class.j2")

data = {
    "class_name": "User",
    "docstring": "用户实体类",
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
print(output)
if not os.path.exists('./output_test'):
    os.mkdir('./output_test')
# with open("./output/%s.py" % i, 'w', encoding='utf-8') as out:
with open("./output_test/User.py", 'w', encoding='utf-8') as out:
    out.write(output)
