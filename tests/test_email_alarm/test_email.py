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
from wechat_notice import EmailNotice
from everyday_wechat.control.airquality.air_quality_aqicn import (
    get_air_quality
)


class TestEmailModel(BaseTestCase):
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

            air_quality = get_air_quality(gf.get('air_quality_city'))

            send_msg = '\n'.join(
                x for x in [calendar_info, weather, horoscope, air_quality, dictum, diff_time, sweet_words] if x)
            print(send_msg)
            print('\n' + '-' * 50 + '\n')

    """
    other_alarm_conf:
      email_config:
        user: 'sfyc1314@163.com'
        password: 'pvQ8sgyCRTyq'
        host: 'smtp.163.com'
    """

    def test_send_email(self):
        ac = config.get('other_alarm_conf', None)
        # if ac:
        email_config = ac.get('email_config', None)
        user = email_config.get('user', None)
        password = email_config.get('password', None)
        host = email_config.get('host', None)
        email_notice = EmailNotice(user=user, password=password, host=host)

        # yy = email_notice.send('title', 'hello world', receivers='sfyc23@qq.com')
        # print(yy)

        girlfriend_infos = config.get('alarm_info').get('girlfriend_infos')
        for gf in girlfriend_infos[:1]:
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
            # email_notice.send('title', send_msg, receivers='sfyc23@qq.com')

    def test_moviebox(self):
        pass