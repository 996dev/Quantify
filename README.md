# 量化

Python Requirements.txt——如何在 Python 中创建和 Pip Install Requirements.txt



- `pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/`

```
(.venv) mac@macdeMacBook-Pro Quantify % 
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

Writing to /Users/mac/.config/pip/pip.conf

```

## 创建 requirements.txt 文件

`pip freeze > requirements.txt`

## 安装

`pip install -r requirements.txt`

## 打包工具

`pip install pyinstaller`

`pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple/`


```git
git rm --cached .idea -r
```

```
pip install pyinstaller
pip install tqsdk -U -i 
pip install PySide6
pip install Jinja2

pip install pigar
pip uninstall pigar

pip install "modin[dask]"
pip install openpyxl
pip install pyecharts
pip install wxauto
pyinstaller main.py --noconsole
```


export YT_DLP_HOME=/usr/local/bin/yt-dlp


## 无法 sh 脚本启动问题
### 1. 编写 setup.py
```py
from setuptools import setup, find_packages

setup(
    name="quantify-tool",      # 包名称（pip install 时用）
    version="0.1",             # 版本号
    packages=find_packages(),  # 自动发现所有包（包含 tool/）
    install_requires=[         # 依赖的其他包（可选）
        # "numpy>=1.20.0",
        # "pandas>=1.3.0",
    ],
)
```

### 2. 以可编辑模式安装包
```bash
pip install -e .
```

### 验证
```Bash
pip list | grep quantify
```
