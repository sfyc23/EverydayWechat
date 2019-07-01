# coding=utf-8

"""
每天定时给多个女友发给微信暖心话
核心代码。
"""
import re
import time
import json
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import platform
import random
import itchat
from itchat.content import *
from everyday_wechat.utils.common import md5_encode
from everyday_wechat.utils.data_collection import (
    get_bot_info,
    get_weather_info,
    get_dictum_info,
    get_diff_time,
    get_calendar_info,
    get_constellation_info
)
from everyday_wechat.utils import config

reply_userNames = []
FILEHELPER_MARK = ['文件传输助手', 'filehelper']  # 文件传输助手标识
FILEHELPER = 'filehelper'
timeCompile = re.compile('^\s*([01]?[0-9]|2[0-3])\s*[：:\-]\s*([0-5]?[0-9])\s*$')


def run():
    """ 主运行入口 """
    conf = config.init()
    # conf = get_yaml()
    if not conf:  # 如果 conf，表示配置文件出错。
        print('程序中止...')
        return
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
    loginCallback = init_wechat
    exitCallback = exit_msg
    for _ in range(2):  # 尝试登录 2 次。
        if platform.system() == 'Windows':
            itchat.auto_login(hotReload=hotReload, loginCallback=loginCallback, exitCallback=exitCallback)
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


def init_wechat():
    """ 初始化微信所需数据 """
    set_system_notice('登录成功')

    # conf = get_yaml()
    itchat.get_friends(update=True)  # 更新好友数据。
    itchat.get_chatrooms(update=True)  # 更新群聊数据。

    # 从config copy ，用于保存新的接口内容。
    myset = config.copy()
    # start---------------------------处理自动回复好友---------------------------start
    relay = myset.get('auto_relay_info')
    if relay.get('is_auto_relay'):
        auto_reply_uuids = []
        for name in relay.get('auto_reply_names'):
            if name.lower() in FILEHELPER_MARK:  # 判断是否文件传输助手
                if FILEHELPER not in reply_userNames:
                    auto_reply_uuids.append(FILEHELPER)
                continue
            friend = get_friend(name)
            if friend:
                auto_reply_uuids.append(friend['UserName'])
            else:
                print('自动回复中的好友昵称『{}』有误。'.format(name))
        relay['auto_reply_uuids'] = set(auto_reply_uuids)
        print('已开启图灵自动回复...')
    # end---------------------------处理自动回复好友---------------------------end

    alarm = myset.get('alarm_info')
    alarm_dict = {}
    if alarm.get('is_alarm'):
        for gi in alarm.get('girlfriend_infos'):
            ats = gi.get('alarm_timed')
            if not ats:
                continue
            uuid_list = []
            # start---------------------------处理好友---------------------------start
            friends = gi.get('wechat_name')
            if isinstance(friends, str):
                friends = [friends]
            if isinstance(friends, list):
                for name in friends:
                    if name.lower() in FILEHELPER_MARK:  # 判断是否文件传输助手
                        uuid_list.append(FILEHELPER)
                        continue
                    name_info = get_friend(name)
                    if not name_info:
                        print('用户昵称{}无效'.format(name))
                    else:
                        uuid_list.append(name_info['UserName'])
            # end---------------------------处理好友---------------------------end

            # start---------------------------群组处理---------------------------start
            group_names = gi.get('group_name')
            if isinstance(group_names, str):
                group_names = [group_names]
            if isinstance(group_names, list):
                for name in group_names:
                    name_info = get_group(name)
                    if not name_info:
                        print('定时任务中的群聊名称『{}』有误。'
                              '(注意：必须要把需要的群聊保存到通讯录)'.format(name))
                    else:
                        uuid_list.append(name_info['UserName'])
            # end---------------------------群组处理---------------------------end

            # start---------------------------定时处理---------------------------start
            if isinstance(ats, str):
                ats = [ats]
            if isinstance(ats, list):
                for at in ats:
                    times = timeCompile.findall(at)
                    if not times:
                        print('时间{}格式出错'.format(at))
                        continue
                    hour, minute = int(times[0][0]), int(times[0][1])
                    temp_dict = {'hour': hour, 'minute': minute, 'uuid_list': uuid_list}
                    temp_dict.update(gi)
                    alarm_dict[md5_encode(str(temp_dict))] = temp_dict
        #   end---------------------------定时处理---------------------------end
        alarm['alarm_dict'] = alarm_dict

    # 将解析的数据保存于config中。
    config.update(myset)
    # print(json.dumps(alarm_dict, ensure_ascii=False))

    # 提醒内容不为空时，启动定时任务
    if alarm_dict:
        init_alarm(alarm_dict)  # 初始化定时任务


def init_alarm(alarm_dict):
    # 定时任务
    scheduler = BackgroundScheduler()
    for key, value in alarm_dict.items():
        scheduler.add_job(send_alarm_msg, 'cron', [key], hour=value['hour'],
                          minute=value['minute'], id=key, misfire_grace_time=10 * 60)
    scheduler.start()
    print('已开启定时发送提醒功能...')
    # print(scheduler.get_jobs())


def send_alarm_msg(key):
    """ 发送定时提醒 """
    print('\n启动定时自动提醒...')
    conf = config.get('alarm_info').get('alarm_dict')

    gf = conf.get(key)
    # print(gf)
    calendar_info = get_calendar_info(gf.get('calendar'))
    dictum = get_dictum_info(gf.get('dictum_channel'))
    weather = get_weather_info(gf.get('city_name'))
    diff_time = get_diff_time(gf.get('start_date'), gf.get('start_date_msg'))
    sweet_words = gf.get('sweet_words')
    horoscope = get_constellation_info(gf.get("horescope"))

    send_msg = '\n'.join(x for x in [calendar_info, weather, horoscope, dictum, diff_time, sweet_words] if x)
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
    try:
        # if not get_yaml().get('is_auto_relay'):
        #     return
        conf = config.get('auto_relay_info')
        if not conf.get('is_auto_relay'):
            return
        # print(json.dumps(msg, ensure_ascii=False))
        # 获取发送者的用户id
        uuid = FILEHELPER if msg['ToUserName'] == FILEHELPER else msg.fromUserName
        # 如果用户id是自动回复列表的人员
        if uuid in conf.get('auto_reply_uuids'):
            receive_text = msg.text  # 好友发送来的消息内容
            # 好友叫啥，用于打印
            nickName = FILEHELPER if uuid == FILEHELPER else msg.user.nickName
            print('\n{}发来信息：{}'.format(nickName, receive_text))
            reply_text = get_bot_info(receive_text, uuid)  # 获取自动回复
            if reply_text:  # 如内容不为空，回复消息
                time.sleep(random.randint(1, 2))  # 休眠一秒，保安全。想更快的，可以直接注释。
                reply_text = reply_text if not uuid == FILEHELPER else '机器人回复：' + reply_text
                itchat.send(reply_text, toUserName=uuid)
                print('回复{}：{}'.format(nickName, reply_text))
            else:
                print('自动回复失败\n')
    except Exception as e:
        print(str(e))


def set_system_notice(text):
    """
    给文件传输助手发送系统日志。
    :param text:日志内容
    :return:None
    """
    if text:
        text = '系统通知：' + text
        itchat.send(text, toUserName=FILEHELPER)


def exit_msg():
    set_system_notice('项目已断开连接')


def get_group(gruop_name, update=False):
    """
    根据群组名获取群组数据
    :param wechat_name: 群组名
    :param update: 强制更新群组数据
    :return: msg
    """
    if update: itchat.get_chatrooms(update=True)
    if not gruop_name: return None
    groups = itchat.search_chatrooms(name=gruop_name)
    if not groups: return None
    return groups[0]


def get_friend(wechat_name, update=False):
    """
    根据用户名获取用户数据
    :param wechat_name: 用户名
    :param update: 强制更新用户数据
    :return: msg
    """
    if update: itchat.get_friends(update=True)
    if not wechat_name: return None
    friends = itchat.search_friends(name=wechat_name)
    if not friends: return None
    return friends[0]


if __name__ == '__main__':
    run()
    pass
    # config.init()
    # init_wechat()
