# coding=utf-8
"""
获取各种请求的调度管理中心
"""
import importlib
import re
from datetime import datetime
from datetime import timedelta

# from everyday_wechat.control.weather.rtweather import get_today_weather
from everyday_wechat.control.weather.sojson import get_sojson_weather
from everyday_wechat.utils.common import (
    WEEK_DICT,
    get_constellation_name,
)
from everyday_wechat.utils import config
from everyday_wechat.control.horoscope.xzw_horescope import get_today_horoscope
# from everyday_wechat.control.calendar.sojson_calendar import get_sojson_calendar
from everyday_wechat.control.calendar.rt_calendar import get_rtcalendar

DICTUM_NAME_DICT = {
    1: 'wufazhuce', 2: 'acib', 3: 'lovelive', 4: 'hitokoto',
    5: 'rtjokes', 6: 'juzimi', 7: 'caihongpi'
}
BOT_NAME_DICT = {
    1: 'tuling123', 2: 'yigeai', 3: 'qingyunke', 4: 'qq_nlpchat',
    5: 'tian_robot', 6: 'ruyiai'
}
# 用于星座的正则表达式
BIRTHDAY_COMPILE = re.compile(r'\-?(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')


def get_dictum_info(channel):
    """
    获取每日一句。
    :return:str
    """
    if not channel:
        return None
    source = DICTUM_NAME_DICT.get(channel, '')
    if source:
        addon = importlib.import_module('everyday_wechat.control.onewords.' + source, __package__)
        dictum = addon.get_one_words()
        # print(dictum)
        return dictum
    return None


def get_weather_info(cityname, is_tomorrow=False):
    """
    获取天气
    :param cityname:str,城市名称
    :return: str,天气情况
    """
    if not cityname:
        return
    # return get_today_weather(cityname)
    return get_sojson_weather(cityname, is_tomorrow)


def get_bot_info(message, userId=''):
    """
    跟机器人互动
    # 优先获取图灵机器人API的回复，但失效时，会使用青云客智能聊天机器人API(过时)
    :param message:str, 发送的话
    :param userId: str, 好友的uid，作为请求的唯一标识。
    :return:str, 机器人回复的话。
    """

    channel = config.get('auto_reply_info').get('bot_channel', 3)
    source = BOT_NAME_DICT.get(channel, 'qingyunke')
    # print(source)
    if source:
        addon = importlib.import_module('everyday_wechat.control.bot.' + source, __package__)
        reply_msg = addon.get_auto_reply(message, userId)
        return reply_msg
    # reply_msg = get_tuling123(message)
    # if not reply_msg:
    #     # reply_msg = get_qingyunke(message)
    #     reply_msg = get_yigeai(message)

    return None


def get_diff_time(start_date, start_msg=''):
    """
    # 在一起，一共多少天了。
    :param start_date:str,日期
    :return: str,eg（宝贝这是我们在一起的第 111 天。）
    """
    if not start_date:
        return None
    rdate = r'^[12]\d{3}[ \/\-](?:0?[1-9]|1[012])[ \/\-](?:0?[1-9]|[12][0-9]|3[01])$'
    start_date = start_date.strip()
    if not re.search(rdate, start_date):
        print('日期填写出错..')
        return
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    day_delta = (datetime.now() - start_datetime).days + 1
    if start_msg and start_msg.count('{}') == 1:
        delta_msg = start_msg.format(day_delta)
    else:
        delta_msg = '宝贝这是我们在一起的第 {} 天。'.format(day_delta)
    return delta_msg


def get_constellation_info(birthday_str, is_tomorrow=False):
    """
    获取星座运势
    :param birthday_str:  "10-12" 或  "1980-01-08" 或 星座名
    :return:
    """
    if not birthday_str:
        return
    const_name = get_constellation_name(birthday_str)
    if not const_name:
        print('星座名填写错误')
        return
    return get_today_horoscope(const_name, is_tomorrow)


def get_calendar_info(calendar=True, is_tomorrow=False, _date=''):
    """ 获取万年历 """
    if not calendar:
        return None
    if not is_tomorrow:
        date = datetime.now().strftime('%Y%m%d')
    else:
        date = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
    return get_rtcalendar(date)

    # else:
    #     time_now = datetime.now()
    #     week = WEEK_DICT[time_now.strftime('%A')]
    #     date = time_now.strftime('%Y-%m-%d')
    #     return '{} {}'.format(date, week)


if __name__ == '__main__':
    config.init()
    text = 'are you ok'
    reply_msg = get_bot_info(text)
    print(reply_msg)
    pass
