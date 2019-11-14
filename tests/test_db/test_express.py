# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019年9月4日12:41:33
Introduction:
"""

from tests import BaseTestCase
# from everyday_wechat.utils import config
from everyday_wechat.utils.db_helper import *
from everyday_wechat.control.moviebox.maoyan_movie_box import get_maoyan_movie_box
from datetime import datetime
from datetime import timedelta
from everyday_wechat.control.express.kdniao_express import get_express_info
import pysnooper


class TestDbExpressModel(BaseTestCase):

    def test_db_get_data(self):

        code = '78109182715352'
        cc = get_express_info(code)
        if cc:
            print(cc)
            print(cc['info'])

    def test_db_get_and_save_data(self):
        uid = '05150520'
        code = '78109182715352'
        cc = get_express_info(code)
        if cc:
            update_express(cc, uid)
            print('保存数据')

    def test_db_find_data(self):
        # uid = '05150520'
        uid = ''
        code = '78109182715352'
        # code = ''
        info = find_express(code, uid)
        if info:
            print(info)

    @pysnooper.snoop()
    def test_all_data(self):
        uid = '05150520'
        code = '78109182715352'
        # code = '102276593571'
        # code = 'JD0001855864185'
        db_data = find_express(code, uid)
        shipper_code, shipper_name = '', ''
        if db_data:
            if not db_data['is_forced_update']:
                print(db_data['info'])
                return
            shipper_code = db_data['shipper_code']
            shipper_name = db_data['shipper_name']

        data = get_express_info(
            code,
            shipper_name=shipper_name,
            shipper_code=shipper_code)
        if data:
            print(data['info'])
            update_express(data, uid)
            return
        else:
            print('未查询到此订单号或者快递物流轨迹')
            return
