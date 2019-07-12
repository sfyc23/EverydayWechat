#! usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/6/23
# Author: snow


import os
from unittest import TestCase
from everyday_wechat.utils import config

here_dir = os.path.dirname(__file__)

class BaseTestCase(TestCase):
    def setUp(self):
        config.init()