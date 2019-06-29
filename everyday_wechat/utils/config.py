import os
import yaml
import copy as mycopy


def init():
    global opts
    opts = get_yaml()
    if opts:
        return True

def get_yaml():
    """
    解析 yaml
    :return: s  字典
    """
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_config.yaml')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.Loader)
        return config
    except Exception as error:
        print(error)
        print('你的 _config.yaml 文件配置出错...')
    return None


def get(key, default=None):
    return opts.get(key, default)


def copy():
    return mycopy.deepcopy(opts)


def set(key, value):
    opts[key] = value


def update(new_opts):
    opts.update(new_opts)

if __name__ == '__main__':
    # init()
    get('is_forced_switch')
