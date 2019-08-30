# coding=utf-8

"""
每天定时给多个女友发给微信暖心话
核心代码。
"""

import time
# import json
import platform
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import itchat
from itchat.content import (
    TEXT
)

from everyday_wechat.utils.data_collection import (
    get_weather_info,
    get_dictum_info,
    get_diff_time,
    get_calendar_info,
    get_constellation_info
)
from everyday_wechat.utils import config
from everyday_wechat.utils.itchat_helper import (
    init_wechat_config,
    set_system_notice,
)
from everyday_wechat.utils.group_helper import (
    handle_group_helper
)
from everyday_wechat.utils.friend_helper import (
    handle_friend
)

__all__ = ['run']


def run():
    """ 主运行入口 """
    # 判断是否登录，如果没有登录则自动登录，返回 False 表示登录失败
    if not is_online(auto_login=True):
        return


def is_online(auto_login=False):
    """
    判断是否还在线。
    :param auto_login: bool,当为 Ture 则自动重连(默认为 False)。
    :return: bool,当返回为 True 时，在线；False 已断开连接。
    """

    def _online():
        """
        通过获取好友信息，判断用户是否还在线。
        :return: bool,当返回为 True 时，在线；False 已断开连接。
        """
        try:
            if itchat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if _online(): return True  # 如果在线，则直接返回 True
    if not auto_login:  # 不自动登录，则直接返回 False
        print('微信已离线..')
        return False

    hotReload = not config.get('is_forced_switch', False)  # 切换微信号，重新扫码。
    loginCallback = init_data
    exitCallback = exit_msg
    for _ in range(2):  # 尝试登录 2 次。
        if platform.system() in ('Windows', 'Darwin'):
            itchat.auto_login(hotReload=hotReload,
                              loginCallback=loginCallback, exitCallback=exitCallback)
            itchat.run(blockThread=True)
        else:
            # 命令行显示登录二维码。
            itchat.auto_login(enableCmdQR=2, hotReload=hotReload, loginCallback=loginCallback,
                              exitCallback=exitCallback)
            itchat.run(blockThread=True)
        if _online():
            print('登录成功')
            return True

    print('登录失败。')
    return False


def init_data():
    """ 初始化微信所需数据 """
    set_system_notice('登录成功')
    itchat.get_friends(update=True)  # 更新好友数据。
    itchat.get_chatrooms(update=True)  # 更新群聊数据。

    init_wechat_config()  # 初始化所有配置内容

    # 提醒内容不为空时，启动定时任务
    alarm_dict = config.get('alarm_info').get('alarm_dict')
    if alarm_dict:
        init_alarm(alarm_dict)  # 初始化定时任务

    print('初始化完成，开始正常工作。')


def init_alarm(alarm_dict):
    """
    初始化定时任务
    :param alarm_dict: 定时相关内容
    """
    # 定时任务
    scheduler = BackgroundScheduler()
    for key, value in alarm_dict.items():
        scheduler.add_job(send_alarm_msg, 'cron', [key], hour=value['hour'],
                          minute=value['minute'], id=key, misfire_grace_time=600)
    scheduler.start()
    # print('已开启定时发送提醒功能...')
    # print(scheduler.get_jobs())


def send_alarm_msg(key):
    """ 发送定时提醒 """
    print('\n启动定时自动提醒...')
    conf = config.get('alarm_info').get('alarm_dict')

    gf = conf.get(key)
    # print(gf)
    is_tomorrow = gf.get('is_tomorrow', False)
    calendar_info = get_calendar_info(gf.get('calendar'), is_tomorrow)
    weather = get_weather_info(gf.get('city_name'), is_tomorrow)
    horoscope = get_constellation_info(gf.get("horescope"), is_tomorrow)
    dictum = get_dictum_info(gf.get('dictum_channel'))
    diff_time = get_diff_time(gf.get('start_date'), gf.get('start_date_msg'))
    sweet_words = gf.get('sweet_words')
    send_msg = '\n'.join(
        x for x in [calendar_info, weather, horoscope, dictum, diff_time, sweet_words] if x)
    # print('\n' + send_msg + '\n')
    if not send_msg or not is_online(): return
    uuid_list = gf.get('uuid_list')
    for uuid in uuid_list:
        time.sleep(1)
        itchat.send(send_msg, toUserName=uuid)
    print('\n定时内容:\n{}\n发送成功...\n\n'.format(send_msg))
    print('自动提醒消息发送完成...\n')


@itchat.msg_register([TEXT])
def text_reply(msg):
    """ 监听用户消息，用于自动回复 """
    handle_friend(msg)
    # print(json.dumps(msg, ensure_ascii=False))


@itchat.msg_register([TEXT], isGroupChat=True)
def text_group(msg):
    """ 监听用户消息，用于自动回复 """
    handle_group_helper(msg)


def exit_msg():
    """ 退出通知 """
    print('程序已退出')


if __name__ == '__main__':
    # run()
    pass
    # config.init()
    # init_wechat()
