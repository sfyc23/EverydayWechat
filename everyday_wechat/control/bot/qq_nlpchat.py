# -*- coding: utf-8 -*- 
"""
Project: HelloWorldPython
Creator: DoubleThunder
Create time: 2019-07-01 23:49
Introduction: 智能闲聊（腾讯）
官网：https://ai.qq.com/product/nlpchat.shtml
免费试用，得申请 app_id，app_key。
"""

import hashlib
from urllib import parse
import time
import random
import string
import requests
from everyday_wechat.utils.common import (
    md5_encode
)
from everyday_wechat.utils import config

URL = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

def get_nlp_textchat(text, userId):
    """
    智能闲聊（腾讯）<https://ai.qq.com/product/nlpchat.shtml>
    接口文档：<https://ai.qq.com/doc/nlpchat.shtml>
    :param text: 请求的话
    :param userId: 用户标识
    :return: str
    """
    try:

        # config.init()
        info = config.get('auto_relay_info')['qqnlpchat_conf']
        app_id = info['app_id']
        app_key = info['app_key']
        if not app_id or not app_key:
            print('app_id 或 app_key 为空，请求失败')
            return

        # 产生随机字符串
        nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 16)))
        time_stamp = int(time.time())  # 时间戳
        params = {
            'app_id': app_id, # 应用标识
            'time_stamp': time_stamp, # 请求时间戳（秒级）
            'nonce_str': nonce_str, # 随机字符串
            'session': md5_encode(userId), # 会话标识
            'question': text  # 用户输入的聊天内容
        }
        # 签名信息
        params['sign'] = getReqSign(params, app_key)
        resp = requests.get(URL, params=params)
        if resp.status_code == 200:
            # print(resp.text)
            content_dict = resp.json()
            if content_dict['ret'] == 0:
                data_dict = content_dict['data']
                return data_dict['answer']
            else:
                print('智能闲聊 获取数据失败:{}'.format(content_dict['msg']))
    except Exception as exception:
        print(str(exception))


def getReqSign(parser, app_key):
    '''
    获取请求签名，接口鉴权 https://ai.qq.com/doc/auth.shtml
    1.将 <key, value> 请求参数对按 key 进行字典升序排序，得到有序的参数对列表 N
    2.将列表 N 中的参数对按 URL 键值对的格式拼接成字符串，得到字符串 T（如：key1=value1&key2=value2），
        URL 键值拼接过程 value 部分需要 URL 编码，URL 编码算法用大写字母，例如 %E8，而不是小写 %e8
    3.将应用密钥以 app_key 为键名，组成 URL 键值拼接到字符串 T 末尾，得到字符串 S（如：key1=value1&key2=value2&app_key = 密钥)
    4.对字符串 S 进行 MD5 运算，将得到的 MD5 值所有字符转换成大写，得到接口请求签名
    :param parser: dect
    :param app_key: str
    :return: str,签名
    '''
    params = sorted(parser.items())
    uri_str = parse.urlencode(params, encoding="UTF-8")
    sign_str = '{}&app_key={}'.format(uri_str, app_key)
    # print('sign =', sign_str.strip())
    hash_md5 = hashlib.md5(sign_str.encode("UTF-8"))
    return hash_md5.hexdigest().upper()

get_auto_reply = get_nlp_textchat

if __name__ == '__main__':
    to_text = '你会爱我吗'
    userId = 'userId'
    # userId = 250
    form_text = get_nlp_textchat(to_text, userId)
    print(form_text)
    # print()
