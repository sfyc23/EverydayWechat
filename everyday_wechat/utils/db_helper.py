# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-12 18:37
Introduction:
"""
import pymongo
from everyday_wechat.utils import config
from functools import wraps
from datetime import datetime

# config.init()

cache_valid_time = 4 * 60 * 60  # 缓存有效时间

is_open_db = config.get('db_config')['is_open_db']
if is_open_db:
    mongodb_conf = config.get('db_config')['mongodb_conf']
    try:
        myclient = pymongo.MongoClient(
            host=mongodb_conf['host'],
            port=mongodb_conf['port'],
            serverSelectionTimeoutMS=10)
        myclient.server_info()  # 查看数据库信息，在这里用于是否连接数据的测试

        wechat_helper_db = myclient["wechat_helper"]
        weather_db = wechat_helper_db['weather']
        user_city_db = wechat_helper_db['user_city']
        perpetual_calendar_db = wechat_helper_db['perpetual_calendar']
        rubbish_db = wechat_helper_db['rubbish_assort']

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(str(err))
        print('数据库连接失败\n')
        is_open_db = False  # 把数据库设为不可用


def db_flag():
    """ 用于数据库操作的 flag 没开启就不进行数据库操作"""

    def _db_flag(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if is_open_db:
                return func(*args, **kwargs)
            else:
                return None

        return wrapper

    return _db_flag


@db_flag()
def udpate_weather(data):
    """
    更新天气数据
    :param data:
    """
    key = {'_date': data['_date'], 'city_name': data['city_name']}
    weather_db.update_one(key, {"$set": data}, upsert=True)


@db_flag()
def udpate_user_city(data):
    """
    更新用户城市信息，用户最后一次查询成功的城市名
    :param data:
    """
    key = {'userid': data['userid']}
    user_city_db.update_one(key, {"$set": data}, upsert=True)


@db_flag()
def find_user_city(uuid):
    """
    找到用户的城市，用户最后一次查询的城市名
    :param uuid:
    :return:
    """
    key = {'userid': uuid}
    data = user_city_db.find_one(key)
    if data:
        return data['city_name']


@db_flag()
def find_weather(date, cityname):
    """
    根据日期与城市名获取天气信息，天气信息有效期为4小时
    :param date: 日期(yyyy-mm-dd)
    :param cityname: 城市名
    :return: 天气信息
    """
    key = {'_date': date, 'city_name': cityname}
    data = weather_db.find_one(key)
    if data:
        diff_second = (datetime.now() - data['last_time']).seconds
        if diff_second <= cache_valid_time:
            return data['weather_info']
    return None


@db_flag()
def update_perpetual_calendar(_date, info):
    """
    更新日历信息
    :param _date: 日期(yyyy-mm-dd)
    :param info: 内容
    :return: None
    """
    key = {'_date': _date}
    data = {
        '_date': _date,
        'info': info,
        'last_time': datetime.now()
    }
    perpetual_calendar_db.update_one(key, {"$set": data}, upsert=True)


@db_flag()
def find_perpetual_calendar(_date):
    """
    查找日历内容
    :param _date: str 日期(yyyy-mm-dd)
    :return: str
    """
    key = {'_date': _date}
    data = perpetual_calendar_db.find_one(key)
    if data:
        return data['info']


@db_flag()
def find_rubbish(name):
    """
    从数据库里查询获取内容
    {'name': '爱群主', 'type': '什么垃圾'}
    """
    key = {'name': name}
    one = rubbish_db.find_one(key, {"_id": 0, "name": 1, "type": 1})
    if one:
        return one['type']
    return None


# 保存进数据库
# 如果有数据，则更新类别
@db_flag()
def update_rubbish(data):
    """
    将垃圾保存数据库
    :param data:
    :return:
    """
    if isinstance(data, str):
        data = [data]
    if isinstance(data, list):
        for d in data:
            key = {'name': d['name']}
            value = {"$set": {"type": d['type']}}
            rubbish_db.update_one(key, value, upsert=True)

# if __name__ == '__main__':
#     uuid = 'uuid'
#     y = find_user_city(uuid)
#     print(y)
#
#     _date = datetime.now().strftime('%Y-%m-%d')
#     cityname = '南京'
#     fw = find_weather(_date, cityname)
#     print(fw)
