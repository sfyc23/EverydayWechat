# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-11 14:56
Introduction:
"""

import itchat
import re

from everyday_wechat.utils import config
from everyday_wechat.utils.common import (
    md5_encode,
    FILEHELPER_MARK,
    FILEHELPER,
)

__all__ = ['init_wechat_config', 'set_system_notice', 'get_group', 'get_friend']

TIME_COMPILE = re.compile(r'^\s*([01]?[0-9]|2[0-3])\s*[：:\-]\s*([0-5]?[0-9])\s*$')


def init_wechat_config():
    """ 初始化微信所需数据 """
    # print('初始化微信所需数据开始..')
    # 从config copy ，用于保存新的接口内容。
    myset = config.copy()
    # start---------------------------处理自动回复好友---------------------------start
    reply = myset.get('auto_reply_info')
    if reply.get('is_auto_reply'):
        if reply.get('is_auto_reply_all'):
            auto_reply_list_key = 'auto_reply_black_list'
            auto_reply_list_uuid_name = 'auto_reply_black_uuids'
        else:
            auto_reply_list_key = 'auto_reply_white_list'
            auto_reply_list_uuid_name = 'auto_reply_white_uuids'
        auto_reply_uuids_list = []
        for name in reply.get(auto_reply_list_key):
            if not name.strip():
                continue
            if name.lower() in FILEHELPER_MARK:  # 判断是否文件传输助手
                auto_reply_uuids_list.append(FILEHELPER)
                continue
            friend = get_friend(name)
            if friend:
                auto_reply_uuids_list.append(friend['UserName'])
            else:
                print('自动回复中的好友昵称『{}』有误。'.format(name))
        reply[auto_reply_list_uuid_name] = set(auto_reply_uuids_list)

        print('已开启图灵自动回复...')
    # end---------------------------处理自动回复好友---------------------------end

    # start ----------------------------------- 群功能初始化 ----------------------------------- start
    helper = myset.get('group_helper_conf')
    if helper.get('is_open'):
        if helper.get('is_all', False):
            group_list_key = 'group_name_black_list'
            group_list_uuid_name = 'group_black_uuids'
        else:
            group_list_key = 'group_name_white_list'
            group_list_uuid_name = 'group_white_uuids'
        group_uuid_list = []
        for name in helper.get(group_list_key):
            if not name.strip():
                continue
            group = get_group(name)
            if group:
                group_uuid_list.append(group['UserName'])
            else:
                print('群助手中的群聊名称『{}』有误。'
                      '(注意：必须要把需要的群聊保存到通讯录)'.format(name))
        helper[group_list_uuid_name] = set(group_uuid_list)
    #   end ----------------------------------- 群功能初始化 ----------------------------------- end

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
                        print('定时提醒中的好友昵称『{}』无效'.format(name))
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
                    times = TIME_COMPILE.findall(at)
                    if not times:
                        print('时间{}格式出错'.format(at))
                        continue
                    hour, minute = int(times[0][0]), int(times[0][1])
                    temp_dict = {'hour': hour, 'minute': minute, 'uuid_list': uuid_list}
                    temp_dict.update(gi)
                    alarm_dict[md5_encode(str(temp_dict))] = temp_dict
        #   end---------------------------定时处理---------------------------end
        alarm['alarm_dict'] = alarm_dict

    # 将解析的数据保存于 config 中。
    config.update(myset)
    # print(json.dumps(alarm_dict, ensure_ascii=False))
    # print('初始化微信所需数据结束..')


def set_system_notice(text):
    """
    给文件传输助手发送系统日志。
    :param text:str 日志内容
    """
    if text:
        text = '系统通知：' + text
        itchat.send(text, toUserName=FILEHELPER)


def get_group(gruop_name, update=False):
    """
    根据群组名获取群组数据
    :param wechat_name:str, 群组名
    :param update: bool 强制更新群组数据
    :return: obj 单个群组信息
    """
    if update: itchat.get_chatrooms(update=True)
    if not gruop_name: return None
    groups = itchat.search_chatrooms(name=gruop_name)
    if not groups: return None
    return groups[0]


def get_friend(wechat_name, update=False):
    """
    根据用户名获取用户数据
    :param wechat_name: str 用户名
    :param update: bool 强制更新用户数据
    :return: obj 单个好友信息
    """
    if update: itchat.get_friends(update=True)
    if not wechat_name: return None
    friends = itchat.search_friends(name=wechat_name)
    if not friends: return None
    return friends[0]
