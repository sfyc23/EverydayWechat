# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-12 19:15
Introduction:
"""

from tests import BaseTestCase
# from everyday_wechat.utils import config
from everyday_wechat.utils.db_helper import *
from everyday_wechat.control.moviebox.maoyan_movie_box import get_maoyan_movie_box
from datetime import datetime
from datetime import timedelta


class TestDbModel(BaseTestCase):

    def test_db_get_data(self):
        # yy = config.get('db_config')['mongodb_conf']
        # host = yy['host']+'dd'
        # port = yy['port']
        # hello = 'mongodb://{host}:{port}/'.format(host=host,port=port)
        #
        # myclient = pymongo.MongoClient(host=host,port=port)
        # dblist = myclient.list_database_names()
        # for db in dblist:
        #     print(db)
        # print('8' * 10, db_helper.is_open_db)
        uuid = '11'
        find_user_city(uuid)

    def test_db_movie(self):
        date_ = datetime.now().strftime('%Y%m%d')

        info = find_movie_box(date_)
        if info:
            print('数据库缓存')
            print(info)
        else:
            mb = get_maoyan_movie_box(date_)
            update_movie_box(date_, mb, is_expired=False)

    def test_db_yesterday_movice(self):
        date_ = (datetime.now() + timedelta(days=-1)).strftime('%Y%m%d')
        print(date_)
