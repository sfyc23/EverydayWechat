# coding=utf-8

import requests
from bs4 import BeautifulSoup
from everyday_wechat.utils.common import SPIDER_HEADERS


def get_wufazhuce_info():
    """
    获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
    :return: str， 一句格言或者短语。
    """
    print('获取 ONE 信息...')
    user_url = 'http://wufazhuce.com/'
    try:
        resp = requests.get(user_url, headers=SPIDER_HEADERS)
        if resp.status_code == 200:
            soup_texts = BeautifulSoup(resp.text, 'lxml')

            # 『one -个』 中的每日一句
            # every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
            every_msg = soup_texts.find('div', class_='fp-one-cita').text #只取当天的这句
            return every_msg
        print('获取 ONE 失败。')
    except Exception as exception:
        print(exception)
        return None
    return None


get_one_words = get_wufazhuce_info

