# Coursable ✅

![GitHub repo size](https://img.shields.io/github/repo-size/KoolShow/Coursable?style=for-the-badge)
![GitHub repo stars](https://img.shields.io/github/stars/KoolShow/Coursable?style=for-the-badge)
![GitHub action status](https://github.com/KoolShow/Coursable/workflows/CI/badge.svg)
![Python](https://img.shields.io/badge/Python-3.13-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![MIT lisence](https://img.shields.io/badge/Lisence-MIT-green?style=for-the-badge)

BJUT课程表解析库, 带有i18n支持

> [!WARNING]
> 本仓库为个人项目, 与BJUT官方无关 \
> 此项目仍处于早期开发阶段, 不保证可用性以及正确性, 欢迎issue和PR

## Features ⚡

- i18n支持 🌐
- 支持第三方json解析库加速 ⚡
- 命令行调用 📝
- 导出ics 🗓️
- ...

## Install 📥

### pip 🚀

```bash
pip install git+github.com/KoolShow/Coursable.git
# or
pip install coursable[...] # url, orjson, ujson, ics
```

### Poetry 📜

```bash
git clone https://github.com/KoolShow/Coursable.git
cd Coursable
poetry install --extras ... # url, orjson, ujson, ics
```

### Wheel 🛞

1. Download the latest wheel from [releases](https://github.com/KoolShow/Coursable/releases)
2. Install it with pip

## Usage 📄

```bash
python -m coursable --help
```

```bash
usage: coursable [-h] [-v] [-i INPUT_FILE] [-c OUTPUT_ICS_FILE]

BJUT course table converter.

options:
  -h, --help            show this help message and exit
  -v, --version         Show the version of the tool.
  -i, --input INPUT_FILE
                        The path to the input file. If not provided, the input will be the default example.
  -c, --ics OUTPUT_ICS_FILE
                        Set output format to ics, and specify the output file path.
```

## Contribute 🛠️

TODO

## Lisence 📃

[MIT](https://github.com/Coursable/blob/master/LICENSE) © Coursable
除examples目录及全部.yml文件无任何授权外, 本项目的所有代码文件均使用MIT许可证授权。
