# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-11 12:03
Introduction:
"""
from tests import BaseTestCase
from everyday_wechat.utils import config
from everyday_wechat.utils.data_collection import *


class TestJobModel(BaseTestCase):
    def test_all_info(self):
        """
        测试获取提醒的所有信息。
        :return:
        """
        girlfriend_infos = config.get('alarm_info').get('girlfriend_infos')
        for gf in girlfriend_infos:
            is_tomorrow = gf.get('is_tomorrow', False)
            calendar_info = get_calendar_info(gf.get('calendar'), is_tomorrow)
            weather = get_weather_info(gf.get('city_name'), is_tomorrow)
            horoscope = get_constellation_info(gf.get("horescope"), is_tomorrow)
            dictum = get_dictum_info(gf.get('dictum_channel'))
            diff_time = get_diff_time(gf.get('start_date'), gf.get('start_date_msg'))
            sweet_words = gf.get('sweet_words')
            send_msg = '\n'.join(x for x in [calendar_info, weather, horoscope, dictum, diff_time, sweet_words] if x)
            print(send_msg)
            print('\n' + '-' * 50 + '\n')
