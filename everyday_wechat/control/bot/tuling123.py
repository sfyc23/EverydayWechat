# coding=utf-8

'''
图灵机器人自动回复
官网：http://www.tuling123.com/
apiKey,userid 需要去官网申请。
'''

import requests
from everyday_wechat.utils.common import (
    get_yaml,
    is_json,
    md5_encode
)

# 图灵机器人错误码集合
TULING_ERROR_CODE_LIST = [
    5000, 6000, 4000, 4001, 4002,
    4003, 4005, 4007, 4100, 4200,
    4300, 4400, 4500, 4600, 4602,
    7002, 8008, 0]
URL = "http://openapi.tuling123.com/openapi/api/v2"


def get_tuling123(text, userId):
    """
    接口地址：(https://www.kancloud.cn/turing/www-tuling123-com/718227)
    获取图灵机器人对话
    :param text: 发送的话
    :param userId: 用户唯一标识（最好用微信好友uuid）
    :return: 对白
    """
    info = get_yaml()['turing_conf']
    apiKey = info['apiKey']

    if not apiKey:
        print('图灵机器人 apikey 为空，请求出错')
        return None
    userId = md5_encode(userId if userId else '250')

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

        print('图灵机器人获取数据失败')
    except Exception as e:
        print(e)
        print('图灵机器人获取数据失败')


get_auto_reply = get_tuling123

if __name__ == '__main__':
    text = '雷军 are you ok?'
    reply = get_auto_reply(text,'WE……………………………………')
    print(reply)
    pass
