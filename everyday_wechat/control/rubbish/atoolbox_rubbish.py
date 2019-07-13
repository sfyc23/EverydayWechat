# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-14 01:02
Introduction: http://www.atoolbox.net/Tool.php?Id=804
"""

import requests
from everyday_wechat.utils.common import SPIDER_HEADERS


def get_atoolbox_rubbish(key):
    """
    # http://www.atoolbox.net/Tool.php?Id=804
    :param key:
    :return:
    """
    params = {'key': key}
    resp = requests.get('http://www.atoolbox.net/api/GetRefuseClassification.php',
                        headers=SPIDER_HEADERS,
                        params=params)

    if resp.status_code == 200:
        # print(resp.text)
        content_dict = resp.json()
        if not content_dict:
            return None, None, None
        return_list = list(content_dict.values())
        _type = ''
        for rl in return_list:
            if key == rl['name']:
                _type = rl['type']
                break
        other = ''
        if not _type:
            other = ' '.join(i['name'] for i in return_list[:6])
        return _type, return_list, other
    return None, None, None
