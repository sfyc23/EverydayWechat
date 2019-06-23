#! usr/bin/env python
# -*- coding: utf-8 -*-

"""
    爬取 星座屋 星座运势
    https://www.xzw.com/
"""

from everyday_wechat.utils.common import SPIDER_HEADERS
import requests
from bs4 import BeautifulSoup


XZW_BASE_URL = "https://www.xzw.com/fortune/"
constellation_dict = {
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

def get_constellation(month, day):
    m = 0
    n = ('摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座')
    d = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
    for i in filter(lambda y: y <= (month, day), d): m += 1
    return n[m % 12]

def get_xzw_data_list(constellation_name):
    ret = []
    print("获取星座屋数据 ...")
    for i in ["/", "/1.html"]:
        req_url = XZW_BASE_URL + constellation_dict[constellation_name] + i
        resp = requests.get(req_url, headers=SPIDER_HEADERS)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, "lxml")
            top_data = soup.select(".c_main")[0]
            name = ""
            date_time = top_data.dd.h4.small.text
            lucky_colour = top_data.dd.ul.find_all("li")[6].text.split("：")[1]
            lucky_num = top_data.dd.ul.find_all("li")[7].text.split("：")[1]

            temp_list = top_data.select(".c_cont")[0].find_all("p")
            detail_list = []
            for detail in temp_list:
                detail_list.append({
                    "name": detail.strong.text,
                    "info": detail.span.text
                })
            if i == "/":
                name = constellation_name + "今日运势"
                print("获取今日星座运势成功！")
            elif i == "/1.html":
                name = constellation_name + "明日运势"
                print("获取明日星座运势成功！")
            temp_dict = {
                "title_name": name,
                "date": date_time,
                "lucky_colour": lucky_colour,
                "lucky_num": lucky_num,
                "detail_info": detail_list
            }
            ret.append(temp_dict)
    return ret


def get_xzw_text(birthday_str):
    """获取今日、明日运势发送文本
        birthday_str :  "10-12" 或  "1980-01-08"
    """
    birthday_list = birthday_str.split("-")
    try:
        if len(birthday_list) == 3:
            month, day = int(birthday_list[1]), int(birthday_list[2])
        elif len(birthday_list) == 2:
            month, day = int(birthday_list[0]), int(birthday_list[1])
    except Exception as e:
        print('您输入的生日格式有误，请确认！（例："1980-01-08" 或 "01-08"）')
        return

    resp = ""
    constellation = get_constellation(month, day)
    data_list = get_xzw_data_list(constellation)

    for item in data_list:
        resp += "\n\n" + item['title_name'] + "（" + item['date'] + "）\n"
        resp += "幸运颜色：%s \n" % item['lucky_colour']
        resp += "幸运数字：%s \n" % item['lucky_num']
        for detail in item['detail_info']:
            resp += "- " + detail['name'] + ": \n"
            resp += detail['info'] + "\n"
    return resp



if __name__ == '__main__':
    print(get_xzw_text("01-22"))



