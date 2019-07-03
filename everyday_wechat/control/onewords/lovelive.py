# coding=utf-8
"""
从土味情话中获取每日一句。
 """
import requests

def get_lovelive_info():
    """
    从土味情话中获取每日一句。
    :return: str,土味情话。
    """
    print('获取土味情话...')
    try:
        resp = requests.get('https://api.lovelive.tools/api/SweetNothings')
        if resp.status_code == 200:
            return resp.text
        print('土味情话获取失败。')
    except requests.exceptions.RequestException as exception:
        print(exception)
        # return None
    return None

get_one_words = get_lovelive_info
