# coding=utf-8
"""
『一个AI』自动回复 (http://www.yige.ai/)
"""
import requests

from main.common import (
    get_yaml,
    is_json,
    md5_encode,
)

# 一个AI错误集合
TULING_ERROR_CODE_LIST = [
    501, 502, 503, 504, 506,
    507, 510]


def get_yigeai(text):
    """
    『一个AI』自动回复 (http://www.yige.ai/)
    :param text: 需要发送的话
    :return:str
    """
    conf = get_yaml()
    token = conf['yigeai_conf']['client_token']
    if not token:
        # print('一个AI token 为空')
        return None

    # 一个字符串token，最多36个字符，用来识别客户端和服务端每个会话参数
    session_id = md5_encode(''.join(conf.get('auto_reply_names')))

    try:
        # print('发出消息:{}'.format(text))
        resp = requests.post('http://www.yige.ai/v1/query',
                             data={'token': token, 'query': text, 'session_id': session_id})
        if resp.status_code == 200 and is_json(resp):
            # print(resp.text)
            re_data = resp.json()
            if re_data['status']['code'] not in TULING_ERROR_CODE_LIST:
                return_text = re_data['answer']
                return return_text
            else:
                error_text = re_data['status']['error_msg']
                print('『一个AI』机器人错误信息：{}'.format(error_text))
        print('『一个AI』机器人发送失败')
        return None
    except Exception as e:
        print(e)
        return None
    return None


get_auto_reply = get_yigeai

if __name__ == '__main__':
    text = '我很想你'
    rt = get_auto_reply(text)
    print('回复：', rt)
    # y = get_yaml().get('auto_reply_names')
    # print(type(y))
