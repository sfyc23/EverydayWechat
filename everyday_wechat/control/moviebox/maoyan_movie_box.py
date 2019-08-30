# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-08-30 12:22
Introduction: 猫眼实时票房 地址：https://piaofang.maoyan.com/dashboard
接口地址：https://box.maoyan.com/promovie/api/box/second.json?beginDate=20190830
"""
import requests

from datetime import datetime


def get_maoyan_movie_box(date='', is_expired=False):
    """
     获取特定日期的实时票房日期
     https://box.maoyan.com/promovie/api/box/second.json?beginDate=20190830#指定日期的节假日及万年历信息
    :param date: str 日期 格式 yyyyMMdd
    :param is_expired
    :rtype str
    """
    date_ = date or datetime.now().strftime('%Y%m%d')

    print('获取 {} 的票房数据...'.format(date_))
    # try:
    resp = requests.get('https://box.maoyan.com/promovie/api/box/second.json?beginDate={}'.format(date_))
    if resp.status_code == 200:
        # print(resp.text)
        content_dict = resp.json()
        if content_dict['success']:
            data_dict = content_dict['data']
            total_box_info = data_dict['totalBoxInfo']
            box_list = data_dict['list']
            box_info_list = []

            for i, r in enumerate(box_list[:10]):
                movice_name = r['movieName']
                box_info = r['boxInfo']
                sumBoxInfo = r['sumBoxInfo']
                box_info_list.append('{}.《{}》({}万，累积:{})'.format(str(i + 1), movice_name, box_info, sumBoxInfo))

            cur_date = datetime.strptime(date_, '%Y%m%d').strftime('%Y{}%m{}%d{}').format('年', '月', '日')

            return_text = "{cur_date} {box_name}\n当日总票房：{total_box_info}万\n{box_info}".format(
                cur_date=cur_date,
                box_name="实时票房" if is_expired else "当日票房",
                total_box_info=total_box_info,
                box_info='\n'.join(box_info_list)
            )

            return return_text
        else:
            print('获取票房失败:{}'.format(content_dict['msg']))
            return None

    print('获取票房失败。')
    # except Exception as exception:
    #     print(str(exception))
    return None


# __date = '20190831'
# dd = get_maoyan_movice_box(__date, is_expired=False)
# print(dd)
