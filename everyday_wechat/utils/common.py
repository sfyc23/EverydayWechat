# coding=utf-8
"""
工具类
"""

import os
import yaml
from simplejson import JSONDecodeError
import hashlib

SPIDER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.87 Safari/537.36',
}

class YamlSetting(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.yaml_setting = self.get_yaml()

    def get_yaml(self):
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

def get_yaml():
    return YamlSetting().yaml_setting

# def get_yaml():
#     """
#     解析 yaml
#     :return: s  字典
#     """
#     path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_config.yaml')
#
#     try:
#         with open(path, 'r', encoding='utf-8') as file:
#             config = yaml.load(file, Loader=yaml.Loader)
#
#         return config
#     except Exception as error:
#         print(error)
#         print('你的 _config.yaml 文件配置出错...')
#     return None


def is_json(resp):
    """
    判断数据是否能被 Json 化。 True 能，False 否。
    :param resp: request.
    :return: bool, True 数据可 Json 化；False 不能 JOSN 化。
    """
    try:
        resp.json()
        return True
    except JSONDecodeError:
        return False

def md5_encode(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    encodedStr = md5.hexdigest().upper()
    return encodedStr

if __name__ == '__main__':
    print(get_yaml())