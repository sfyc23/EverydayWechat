# coding=utf-8

'''
图灵机器人自动回复
官网：http://www.tuling123.com/
apiKey,userid 需要去官网申请。
'''

import requests

from main.common import (
    get_yaml,
    is_json,
)
# 图灵机器人错误码集合
TULING_ERROR_CODE_LIST = [
    5000, 6000, 4000, 4001, 4002,
    4003, 4005, 4007, 4100, 4200,
    4300, 4400, 4500, 4600, 4602,
    7002, 8008, 0]
URL = "http://openapi.tuling123.com/openapi/api/v2"


def get_tuling123(text):
    """
    获取
    :param text:
    :return:
    """
    info = get_yaml()['turing_conf']
    apiKey = info['apiKey']
    userId = info['userId']
    if not apiKey or not userId: return None
    content = {
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': apiKey,
            'userId': userId
        }
    }
    try:
        # print('发出消息:{}'.format(text))
        resp = requests.post(URL, json=content)
        if resp.status_code == 200 and is_json(resp):
            # print(resp.text)
            re_data = resp.json()
            if re_data['intent']['code'] not in TULING_ERROR_CODE_LIST:
                return_text = re_data['results'][0]['values']['text']
                return return_text
            else:
                error_text = re_data['results'][0]['values']['text']
                print('图灵机器人错误信息：{}'.format(error_text))
        print('图灵机器人发送失败')
        return None
    except Exception as e:
        print(e)
        return None
    return None


get_auto_reply = get_tuling123

if __name__ == '__main__':
    text = '雷军 are you ok?'
    reply = get_auto_reply(text)
    print(reply)
    pass
