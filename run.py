# coding=utf-8
"""
程序运行入口
"""

import sys
import re
from datetime import datetime

try:
    from everyday_wechat import __version__

    print('EverydayWechat 程序版本号：{}'.format(__version__))
    _date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('当前时间：{}'.format(_date))
except Exception as exception:
    print(str(exception))
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 everyday_wechat 文件夹是否存在')
    exit(1)


def run():
    """ 主程序入口"""

    # 判断当前环境是否为 python 3
    if sys.version_info[0] == 2:
        print('此项目不支持 Python 2 版本！')
        return

    # 检查依赖库是否都已经安装上
    try:
        import itchat
        import apscheduler
        import requests
        from bs4 import BeautifulSoup
        if itchat.__version__ != '1.3.10':
            print('请将 itchat 的版本升级至 1.3.10！')
            return

    except (ModuleNotFoundError, ImportError) as error:
        if isinstance(error, ModuleNotFoundError):
            no_modules = re.findall(r"named '(.*?)'$", str(error))
            if no_modules:
                print('当前运行环境缺少 {} 库'.format(no_modules[0]))
            print(str(error))
        elif isinstance(error, ImportError):
            print('当前运行环境引入库出错')
            print(str(error))
        return

    # 用于判断数据库功能是否开启
    try:
        from everyday_wechat.utils import config
        from everyday_wechat.utils.db_helper import is_open_db
        if not is_open_db:
            print('数据库未开启或启动失败')
    except Exception as exception:
        print(str(exception))
        return

    from everyday_wechat import main
    main.run()


if __name__ == '__main__':
    run()
