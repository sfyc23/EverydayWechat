# coding=utf-8
"""
用于管理缓存的配置数据
使用前必须先调用 init() 。
"""
import os
import copy as mycopy
import yaml

def init():
    """
    将 yaml 里的配置文件导入到 config.py 中
    :return: bool ，true 表示数据导入成功。
    """
    global opts
    opts = get_yaml()
    if opts:
        return True
    return False

def get_yaml():
    """
    解析 yaml
    :return: s  字典
    """
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_config.yaml')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file, Loader=yaml.Loader)
        return config
    except Exception as exception:
        print(str(exception))
        print('你的 _config.yaml 文件配置出错...')
    return None

def set(key, value):
    """ 通过 key 设置某一项值 """
    opts[key] = value

def get(key, default=None):
    """ 通过 key 获取值 """
    return opts.get(key, default)

def copy():
    """ 复制配置 """
    return mycopy.deepcopy(opts)

def update(new_opts):
    """ 全部替换配置 """
    opts.update(new_opts)

if __name__ == '__main__':
    # init()
    # get('is_forced_switch')
    pass
