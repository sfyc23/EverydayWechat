# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-11 12:55
Introduction: 群消息处理
"""
import itchat
import re
from datetime import datetime

from everyday_wechat.utils import config
from everyday_wechat.control.calendar.rt_calendar import get_rtcalendar
from everyday_wechat.utils.data_collection import (
    get_weather_info,
    get_bot_info,
    get_calendar_info,
)
from everyday_wechat.utils.db_helper import (
    find_perpetual_calendar,
    find_user_city,
    find_weather,
    udpate_user_city,
    udpate_weather,
    update_perpetual_calendar
)
# import pysnooper

at_compile = re.compile(r'(@.*?\s{1}).*?')
tomorrow_compile = r'明[日天]'
calendar_complie = r'\s*(?:日|万年)历\s*'
weather_compile = r'^(?:\s*天气\s*(\S+?)|\s*(\S*?)\s*天气\s*)$'
help_complie = r'^(?:帮忙|帮助|help)\s*$'
punct_complie = r'[^a-zA-z\u4e00-\u9fa5]+$' #去除句子最后面的标点

common_msg = '@{ated_name}\u2005 {text}'
weather_error_msg = '@{ated_name}\u2005\n未找到『{city}』城市的相关信息'


help_group_content = """
群助手功能：
1.输入：天气+城市名；
2.输入：万年历；
更多功能：请输入 help/帮助。
"""

# @pysnooper.snoop()
def handle_group_helper(msg):
    """
    处理群消息
    :param msg:
    :return:
    """
    conf = config.get('group_helper_conf')
    if not conf.get('is_open'):
        return
    text = msg['Text']

    # 如果开启了 『艾特才回复』，而群用户又没有艾特你。不处理消息
    if conf.get('is_at') and not msg.isAt:
        return

    uuid = msg.fromUserName # 群 uid
    ated_uuid = msg.actualUserName # 艾特你的用户的uuid
    ated_name = msg.actualNickName # 艾特你的人的群里的名称

    is_all = conf.get('is_all', False)
    user_uuids = conf.get('group_black_uuids') if is_all else conf.get('group_white_uuids')
    # 开启回复所有群，而用户是黑名单，不处理消息
    if is_all and uuid in user_uuids:
        return

    # 未回复所有群，而用户不是白名单，不处理消息
    if not is_all and uuid not in user_uuids:
        return
    # 去掉 at 标记
    text = at_compile.sub('', text)

    # 如果是帮助
    helps = re.findall(help_complie,text,re.I)
    if helps:
        itchat.send(help_group_content, uuid)
        return

    # 是否是明天，用于日历，天气，星座查询
    is_tomorrow = re.findall(tomorrow_compile, text)
    if is_tomorrow:
        is_tomorrow = True
        htext = re.sub(tomorrow_compile, '', text)
    else:
        is_tomorrow = False
        htext = text

    htext = re.sub(punct_complie, '', htext) # 去句末的标点

    # 已开启天气查询，并包括天气关键词
    if conf.get('is_weather'):
        citys = re.findall(weather_compile, htext)
        if citys:
            for x in citys[0]:
                city = x
                if city:
                    break
            else:
                city = find_user_city(ated_uuid)
                if not city:
                    city = get_city_by_uuid(ated_uuid)
            if city:
                _date = datetime.now().strftime('%Y-%m-%d')
                weather_info = find_weather(_date, city)
                if weather_info:
                    retext = common_msg.format(ated_name=ated_name, text=weather_info)
                    itchat.send(retext, uuid)
                    return

                weather_info = get_weather_info(city)
                if weather_info:
                    # print(ated_name, city, retext)
                    retext = common_msg.format(ated_name=ated_name, text=weather_info)
                    itchat.send(retext, uuid)

                    data = {
                        '_date': _date,
                        'city_name': city,
                        'weather_info': weather_info,
                        'userid': ated_uuid,
                        'last_time': datetime.now()
                    }
                    udpate_weather(data)
                    # userid,city_name,last_time,group_name udpate_weather_city
                    data2 = {
                        'userid': ated_uuid,
                        'city_name': city,
                        'last_time': datetime.now()
                    }
                    udpate_user_city(data2)
                    return
                else:
                    weather_error_msg = '@{ated_name}\u2005\n未找到『{city}』城市的相关信息'
                    retext = weather_error_msg.format(ated_name=ated_name, city=city)
                    itchat.send(retext, uuid)
                    return
            return

    # 已开启日历，并包含日历
    if conf.get('is_calendar'):
        if re.findall(calendar_complie, htext):
            _date = datetime.now().strftime('%Y-%m-%d')
            cale_info = find_perpetual_calendar(_date)
            if cale_info:
                retext = common_msg.format(ated_name=ated_name, text=cale_info)
                itchat.send(retext, uuid)
                return

            rt_date = datetime.now().strftime('%Y%m%d')
            cale_info = get_rtcalendar(rt_date)
            if cale_info:
                retext = common_msg.format(ated_name=ated_name, text=cale_info)
                itchat.send(retext, uuid)
                update_perpetual_calendar(_date, cale_info)
                return
            return

    # 其他结果都没有匹配到，走自动回复的路
    if conf.get('is_auto_reply'):
        reply_text = get_bot_info(text, ated_uuid)  # 获取自动回复
        if reply_text:  # 如内容不为空，回复消息
            reply_text = common_msg.format(ated_name=ated_name, text=reply_text)
            itchat.send(reply_text, uuid)
            print('回复{}：{}'.format(ated_name, reply_text))
        else:
            print('自动回复失败\n')


# 通过用户id找好友
def get_city_by_uuid(uid):
    """
    通过用户的uid得到用户的城市
    最好是与机器人是好友关系
    """
    itchat.get_friends(update=True)
    info = itchat.search_friends(userName=uid)
    # print('info:'+str(info))
    if not info:
        return None
    city = info.city
    # print('city:'+city)
    return city
