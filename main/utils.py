# coding=utf-8

import importlib
from datetime import datetime

from weather.sojson import get_today_weather
# from weather.rtweather import get_rttodayweather
# from bot.qingyunke import get_qingyunke
# from bot.tuling123 import get_tuling123
# from bot.yigeai import get_yigeai
from main.common import (
    get_yaml
)
from horoscope.spider_script import get_constellation, get_xzw_data_list

DICTUM_NAME_DICT = {1: 'wufazhuce', 2: 'acib', 3: 'lovelive', 4: 'hitokoto', 5: 'rtjokes', 6: 'scapy'}
BOT_NAME_DICT = {1: 'tuling123', 2: 'yigeai', 3: 'qingyunke'}


def get_dictum_info(channel):
    """
    获取每日提醒。
    :return:str
    """
    if not channel:
        return None
    source = DICTUM_NAME_DICT.get(channel, '')
    if source:
        addon = importlib.import_module('onewords.' + source, __package__)
        dictum = addon.get_one_words()
        # print(dictum)
        return dictum
    return None


def get_weather_info(cityname):
    """
    获取天气
    :param cityname:str,城市名称
    :return: str,天气情况
    """
    if not cityname:
        return
    return get_today_weather(cityname)
    # return get_rttodayweather(cityname)


def get_bot_info(message, userId=''):
    """
    获取自动回复的话。
    # 优先获取图灵机器人API的回复，但失效时，会使用青云客智能聊天机器人API(过时)
    :param message:str, 发送的话
    :return:str, 回复的话
    """
    channel = get_yaml().get('bot_channel', 3)
    source = BOT_NAME_DICT.get(channel, 'qingyunke')
    if source:
        addon = importlib.import_module('bot.' + source, __package__)
        reply_msg = addon.get_auto_reply(message, userId)
        return reply_msg
    # reply_msg = get_tuling123(message)
    # if not reply_msg:
    #     # reply_msg = get_qingyunke(message)
    #     reply_msg = get_yigeai(message)

    return None


def get_diff_time(start_date):
    """
    # 在一起，一共多少天了。
    :param start_date:str,日期
    :return: str,eg（宝贝这是我们在一起的第 111 天。）
    """
    if not start_date:
        return None
    try:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        day_delta = (datetime.now() - start_datetime).days + 1
        delta_msg = '宝贝这是我们在一起的第 {} 天。'.format(day_delta)
    except Exception as exception:
        print(exception)
        delta_msg = None
    return delta_msg


def get_xzw_info(birthday_str):
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
        resp += "\n\n" + item['title_name'] + "  " + item['date'] + "\n"
        resp += "幸运颜色：%s \n" % item['lucky_colour']
        resp += "幸运数字：%s \n" % item['lucky_num']
        for detail in item['detail_info']:
            resp += "- " + detail['name'] + ": \n"
            resp += detail['info'] + "\n"
    return resp


if __name__ == '__main__':
    text = 'are you ok'
    reply_msg = get_bot_info(text)
    print(reply_msg)
    pass
