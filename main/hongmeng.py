# coding=utf-8

"""
每天定时给多个女友发给微信暖心话
核心代码。
"""
import os
import time
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
import itchat
from itchat.content import TEXT
from main.common import (
    get_yaml
)
from main.utils import (
    get_bot_info,
    get_weather_info,
    get_dictum_info,
    get_diff_time,
)

reply_name_uuid_list = []
# fire the job again if it was missed within GRACE_PERIOD
GRACE_PERIOD = 15 * 60


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
        return False

    is_forced_switch = get_yaml().get('is_forced_switch', True)
    for _ in range(2):  # 登陆，尝试 2 次。
        # 如果需要切换微信，删除 hotReload=True
        if os.environ.get('MODE') == 'server':
            # 命令行显示登录二维码。
            itchat.auto_login(enableCmdQR=2, hotReload=is_forced_switch)
        else:
            itchat.auto_login(hotReload=is_forced_switch)
        if _online():
            print('登录成功')
            return True

    print('登录失败。')
    return False


@itchat.msg_register([TEXT])
def text_reply(msg):
    """ 监听用户消息 """
    try:
        # print(msg)
        uuid = msg.fromUserName
        if uuid in reply_name_uuid_list:
            receive_text = msg.text  # 好友发送来的消息
            # 通过图灵 api 获取要回复的内容。
            reply_text = get_bot_info(receive_text)
            time.sleep(1)  # 休眠一秒，保安全，想更快的，可以直接用。
            if reply_text:  # 如内容不为空，回复消息
                msg.user.send(reply_text)  # 发送回复
                print('\n{}发来信息：{}\n回复{}：{}'
                      .format(msg.user.nickName, receive_text, msg.user.nickName, reply_text))
            else:
                print('{}发来信息：{}\t自动回复失败'
                      .format(msg.user.nickName, receive_text))
    except Exception as e:
        print(str(e))


def init_reply():
    """
    初始化自动回复相关数据。
    :return:
    """
    conf = get_yaml()
    for name in conf.get('auto_reply_names', None):
        friends = itchat.search_friends(name=name)
        if not friends:  # 如果用户列表为空，表示用户昵称填写有误。
            print('昵称『{}』有误。'.format(name))
            break
        name_uuid = friends[0].get('UserName')  # 取第一个用户的 uuid。
        if name_uuid not in reply_name_uuid_list:
            reply_name_uuid_list.append(name_uuid)


def init_alarm():
    """ 初始化定时提醒 """
    alarm_info = get_yaml().get('alarm_info', None)
    if not alarm_info: return
    is_alarm = alarm_info.get('is_alarm', False)
    if not is_alarm: return
    alarm_timed = alarm_info.get('alarm_timed', None)
    if not alarm_timed: return
    hour, minute = [int(x) for x in alarm_timed.split(':')]

    # 定时任务
    scheduler = BlockingScheduler()
    # 每天9：30左右给女朋友发送每日一句
    scheduler.add_job(get_alarm_msg, 'cron', hour=hour,
                      minute=minute, misfire_grace_time=GRACE_PERIOD)

    # 每隔 2 分钟发送一条数据用于测试。
    # scheduler.add_job(get_alarm_msg, 'interval', seconds=120)

    print('已开启定时发送提醒功能...')
    scheduler.start()


def get_alarm_msg():
    """ 定时提醒内容 """
    conf = get_yaml()
    for gf in conf.get('girlfriend_infos'):
        dictum = get_dictum_info(gf.get('dictum_channel'))
        weather = get_weather_info(gf.get('city_name'))
        diff_time = get_diff_time(gf.get('start_date'))
        sweet_words = gf.get('sweet_words')
        send_msg = '\n'.join(x for x in [dictum, weather, diff_time, sweet_words] if x)
        print(send_msg)
        if send_msg and is_online():
            wechat_name = gf.get('wechat_name')
            authors = itchat.search_friends(nickName=wechat_name)
            if authors:
                authors[0].send(send_msg)
                print('\n定时给『{}』发送的内容是:\n{}\n发送成功...\n'.format(wechat_name, send_msg))
            else:
                print('定时提醒发送失败，微信名 {} 失效。'.format(wechat_name))


def run():
    """ 主运行入口 """
    if not is_online(auto_login=True):
        print('登录失败')
        return
    conf = get_yaml()
    if conf.get('is_auto_relay', False):
        def _itchatRun():
            itchat.run()

        init_reply()
        thread = threading.Thread(target=_itchatRun, name='LoopThread')
        thread.start()
        print('已开启图灵自动回复...')
        init_alarm()
        thread.join()
    else:
        init_alarm()


if __name__ == '__main__':
    # run()
    # get_alarm_msg()
    pass
