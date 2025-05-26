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
