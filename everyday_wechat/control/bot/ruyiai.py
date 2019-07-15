# -*- coding: utf-8 -*-
"""
Project: HelloWorldPython
Creator: DoubleThunder
Create time: 2019-07-02 02:46
Introduction: 海知智能 <https://ruyi.ai/> 功能很强大，不仅仅用于聊天。需申请 key，免费
"""
import requests
from everyday_wechat.utils import config
from everyday_wechat.utils.common import (
    md5_encode
)

__all__ = ['get_ruyiai_bot']

URL = 'http://api.ruyi.ai/v1/message'

def get_ruyiai_bot(text, userId):
    """
    海知智能 文档说明：<http://docs.ruyi.ai/502931>
    :param text: str 需要发送的话
    :param userId: str 用户标识
    :return: str 机器人回复
    """
    try:
        # config.init()
        info = config.get('auto_reply_info')['ruyi_conf']
        app_key = info['app_key']
        if not app_key:
            print('海知智能 api_key 为空，请求失败')
            return

        params = {'q': text, 'user_id': md5_encode(userId), 'app_key': app_key}
        resp = requests.get(URL, headers={'Content-Type': 'application/json'}, params=params)
        if resp.status_code == 200:
            # print(resp.text)
            content_dict = resp.json()
            if content_dict['code'] in (0, 200):
                outputs = content_dict['result']['intents'][0]['outputs']
                reply_text = outputs[0]['property']['text']
                # print(reply_text)
                return reply_text
            else:
                print('海知智能 获取数据失败:{}'.format(content_dict['msg']))
                return
        print('海知智能 获取数据失败')
        return None
    except Exception as exception:
        print(str(exception))


get_auto_reply = get_ruyiai_bot

if __name__ == '__main__':
    # text = '我要飞的更高'
    # userid = '250'
    # from_text = get_auto_reply(text, userid)
    # print(from_text)
    pass
