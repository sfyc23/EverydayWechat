# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-18 14:07
Introduction:
"""
from unittest import TestCase

from everyday_wechat.control.onewords.wufazhuce import get_wufazhuce_info


class BaseTestCase(TestCase):
    def test_get_wufazhuce_(self):
        ok = get_wufazhuce_info()
        print(ok)
