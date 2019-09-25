# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-12 23:07
Introduction: 处理好友消息内容
"""

import time
import random
import itchat
from everyday_wechat.utils import config
from everyday_wechat.utils.data_collection import (
    get_bot_info,
)
from everyday_wechat.utils.common import (
    FILEHELPER,
)

__all__ = ['handle_friend']


def handle_friend(msg):
    """ 处理好友信息 """
    try:

        # 自己通过手机微信发送给别人的消息(文件传输助手除外)不作处理。
        if msg['FromUserName'] == config.get('wechat_uuid') and msg['ToUserName'] != FILEHELPER:
            return

        conf = config.get('auto_reply_info')
        if not conf.get('is_auto_reply'):
            return
        # 获取发送者的用户id
        uuid = FILEHELPER if msg['ToUserName'] == FILEHELPER else msg['FromUserName']
        is_all = conf.get('is_auto_reply_all')
        auto_uuids = conf.get('auto_reply_black_uuids') if is_all else conf.get('auto_reply_white_uuids')
        # 开启回复所有人，当用户是黑名单，不回复消息
        if is_all and uuid in auto_uuids:
            return

        # 关闭回复所有人，当用户不是白名单，不回复消息
        if not is_all and uuid not in auto_uuids:
            return

        receive_text = msg.text  # 好友发送来的消息内容
        # 好友叫啥，用于打印
        nick_name = FILEHELPER if uuid == FILEHELPER else msg.user.nickName
        print('\n{}发来信息：{}'.format(nick_name, receive_text))
        reply_text = get_bot_info(receive_text, uuid)  # 获取自动回复
        if reply_text:  # 如内容不为空，回复消息
            time.sleep(random.randint(1, 2))  # 休眠一秒，保安全。想更快的，可以直接注释。

            prefix = conf.get('auto_reply_prefix', '')  # 前缀
            if prefix:
                reply_text = '{}{}'.format(prefix, reply_text)

            suffix = conf.get('auto_reply_suffix', '')  # 后缀
            if suffix:
                reply_text = '{}{}'.format(reply_text, suffix)

            itchat.send(reply_text, toUserName=uuid)
            print('回复{}：{}'.format(nick_name, reply_text))
        else:
            print('自动回复失败\n')
    except Exception as exception:
        print(str(exception))
