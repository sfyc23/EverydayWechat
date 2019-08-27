# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-08-27 11:37
Introduction: 思知机器人，接口地址:<https://www.ownthink.com/> userid 可为空
"""
import re
import requests
from everyday_wechat.utils import config
from everyday_wechat.utils.common import (
    md5_encode
)

__all__ = ['get_auto_reply', 'get_ownthink_robot']


def get_ownthink_robot(text, userid):
    """
    思知机器人，接口地址:<https://www.ownthink.com/>
    https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken=姚明多高啊？
    :param text: 发出的消息
    :param userid: 收到的内容
    :return:
    """
    try:
        # config.init()
        info = config.get('auto_reply_info')['txapi_conf']
        app_key = info.get('app_key', '')
        if not re.findall(r'^[0-9a-z]{20,}$', app_key):  # 验证 app_key 是否有效果
            app_key = ''

        params = {
            'appid': app_key,
            'userid': md5_encode(userid),
            'spoken': text
        }
        url = 'https://api.ownthink.com/bot'
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            print(resp.text)
            content_dict = resp.json()
            if content_dict['message'] == 'success':
                data = content_dict['data']
                if data['type'] == 5000:
                    reply_text = data['info']['text']
                    return reply_text
                else:
                    print('返回的数据不是文本数据！')
            else:
                print('思知机器人获取数据失败:{}'.format(content_dict['msg']))

        print('获取数据失败')
        return None
    except Exception as exception:
        print(str(exception))


get_auto_reply = get_ownthink_robot

if __name__ == '__main__':
    text = '大胸'
    userid = '250'
    from_text = get_ownthink_robot(text, userid)
    print(from_text)
