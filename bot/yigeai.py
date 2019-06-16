#
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
TULING_ERROR_CODE_LIST = ['501', '502', '503', '504', '507', '510']

def get_yigeai(text, userid):
    """
    『一个AI』自动回复 (http://www.yige.ai/)
    接口说明：http://docs.yige.ai/Query%E6%8E%A5%E5%8F%A3.html
    :param text:str, 需要发送的话
    :userid:str,机器唯一标识
    :return:str
    """
    conf = get_yaml()
    token = conf['yigeai_conf']['client_token']
    if not token:
        print('错误 .一个「AI」token 为空')
        return None
    session_id = md5_encode(userid)
    try:
        # print('发出消息:{}'.format(text))
        resp = requests.post('http://www.yige.ai/v1/query',
                             data={'token': token, 'query': text, 'session_id': session_id})
        if resp.status_code == 200 and is_json(resp):
            # print(resp.text)
            re_data = resp.json()
            code = re_data['status']['code']
            # 错误码返回有时是数字，有点是str。一起做处理
            if code and str(code) not in TULING_ERROR_CODE_LIST:
                return_text = re_data['answer']
                return return_text
            else:
                error_text = re_data['status']['error_type']
                print('『一个AI』机器人错误信息：{}'.format(error_text))
        print('『一个AI』机器人获取数据失败')
        return None
    except Exception as e:
        print(e)
        print('『一个AI』机器人获取数据失败')
        return None
    return None


get_auto_reply = get_yigeai

if __name__ == '__main__':
    text = '自动机器人'
    rt = get_auto_reply(text)
    print('回复：', rt)
    # y = get_yaml().get('auto_reply_names')
    # print(type(y))
