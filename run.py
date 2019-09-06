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
            print('当前 itchat 版本为：{} ，本项目需要 itchat 的版本为 1.3.10。请升级至最新版本！\n'
                  '升级方法 1：pip install itchat --upgrade \n'
                  '或者方法 2: pip install -U itchat'.format(itchat.__version__))
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
            print('数据库未开启或启动失败！但数据库功能不会影响项目正常运行，主要用于群助手查询数据缓存。')
    except Exception as exception:
        print(str(exception))
        return

    print('所有环境配置 OK ..')
    from everyday_wechat import main
    main.run()


if __name__ == '__main__':
    run()
