#! usr/bin/env python
# -*- coding: utf-8 -*-
"""
    爬取 星座屋 星座运势
    https://www.xzw.com/
"""
import re
from functools import reduce
import requests
from bs4 import BeautifulSoup
from everyday_wechat.utils.common import SPIDER_HEADERS

__all__ = ['get_xzw_horoscope', 'get_today_horoscope']

XZW_BASE_URL_TODAY = "https://www.xzw.com/fortune/{}"
XZW_BASE_URL_TOMORROW = "https://www.xzw.com/fortune/{}/1.html"
CONSTELLATION_DICT = {
    "白羊座": "aries",
    "金牛座": "taurus",
    "双子座": "gemini",
    "巨蟹座": "cancer",
    "狮子座": "leo",
    "处女座": "virgo",
    "天秤座": "libra",
    "天蝎座": "scorpio",
    "射手座": "sagittarius",
    "摩羯座": "capricorn",
    "水瓶座": "aquarius",
    "双鱼座": "pisces",
}
def get_xzw_horoscope(name, is_tomorrow=False):
    '''
    获取星座屋(https://www.xzw.com)的星座运势
    :param name: 星座名称
    :return:
    '''
    if not name in CONSTELLATION_DICT:
        print('星座输入有误')
        return
    try:
        const_code = CONSTELLATION_DICT[name]

        req_url = XZW_BASE_URL_TOMORROW.format(const_code) if is_tomorrow \
            else XZW_BASE_URL_TODAY.format(const_code)

        resp = requests.get(req_url, headers=SPIDER_HEADERS)
        if resp.status_code == 200:
            html = resp.text
            lucky_num = re.findall(r'<label>幸运数字：</label>(.*?)</li>', html)[0]
            lucky_color = re.findall(r'<label>幸运颜色：</label>(.*?)</li>', html)[0]
            detail_horoscope = re.findall(r'<p><strong class="p1">.*?</strong><span>(.*?)</span></p>', html)[0]
            if is_tomorrow:
                detail_horoscope = detail_horoscope.replace('今天','明天')

            return_text = '{name}{_date}运势\n【幸运颜色】{color}\n【幸运数字】{num}\n【综合运势】{horoscope}'.format(
                _date='明日' if is_tomorrow else '今日',
                name=name,
                color=lucky_color,
                num=lucky_num,
                horoscope=detail_horoscope
            )
            return return_text
    except Exception as exception:
        print(str(exception))


get_today_horoscope = get_xzw_horoscope

if __name__ == '__main__':
    # print (get_constellation(3, 10))
    # print(get_xzw_text("03-18"))
    is_tomorrow = True
    print(get_xzw_horoscope("水瓶座",is_tomorrow))
