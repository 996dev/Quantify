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

pyinstaller main.py --noconsole
```


export YT_DLP_HOME=/usr/local/bin/yt-dlp
