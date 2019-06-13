# coding=utf-8

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.87 Safari/537.36',
}

def get_wufazhuce_info():
    """
    获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
    :return: str， 一句格言或者短语。
    """
    print('获取格言信息...')
    user_url = 'http://wufazhuce.com/'
    try:
        resp = requests.get(user_url, headers=HEADERS)
        if resp.status_code == 200:
            soup_texts = BeautifulSoup(resp.text, 'lxml')
            # 『one -个』 中的每日一句
            every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
            return every_msg
        print('每日一句获取失败。')
    except Exception as exception:
        print(exception)
        return None
    return None


get_one_words = get_wufazhuce_info
