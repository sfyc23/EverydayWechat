"""
每天定时给多个女友发给微信暖心话
核心代码。
"""
import os
import time
from datetime import datetime
import itchat
from itchat.content import TEXT
import requests
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from simplejson import JSONDecodeError
import threading

import city_dict

# fire the job again if it was missed within GRACE_PERIOD
GRACE_PERIOD = 15 * 60
reply_name_uuid_list = []
tuling_apikey, tuling_userid = '', ''

TULING_ERROR_CODE_LIST = [ # 图灵错误码
    5000, 6000, 4000, 4001, 4002,
    4003, 4005, 4007, 4100, 4200,
    4300, 4400, 4500, 4600, 4602,
    7002, 8008, 0]


class GFWeather:
    """
    每日天气与提醒。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36',
    }
    dictum_channel_name = {1: 'ONE●一个', 2: '词霸(每日英语)', 3: '土味情话', 4: '一言'}

    def __init__(self):
        self.girlfriend_list, self.alarm_hour, self.alarm_minute, self.dictum_channel, self.is_turing = self.get_init_data()

    def get_init_data(self):
        """
        初始化基础数据。
        :return: (dict,int,int,int,bool)
            1.dict 需要发送的用户的信息；
            2.int 时；
            3.int 分；
            4.int 格言渠道。{1: 'ONE●一个', 2: '词霸(每日英语)', 3: '土味情话', 4: '一言'}
            5.bool 是否开启自动回复图灵机器人。
        """
        with open('_config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.Loader)

        alarm_timed = config.get('alarm_timed').strip()
        init_msg = '每天定时发送时间：{}\n'.format(alarm_timed)

        dictum_channel = config.get('dictum_channel', -1)
        init_msg += '格言获取渠道：{}\n'.format(self.dictum_channel_name.get(dictum_channel, '无'))

        # 是否开启图灵
        turing_conf = config.get('turing_conf')
        is_turing = False
        if turing_conf:
            is_turing = turing_conf.get('is_turing')
            if is_turing:
                apikey = turing_conf.get('apiKey')
                userId = turing_conf.get('userId')
                if apikey and userId:
                    global tuling_apikey, tuling_userid
                    tuling_apikey = apikey
                    tuling_userid = userId
                else:
                    print('apikey 与 userid 不能为空')
                    is_turing = False

        girlfriend_list = []
        girlfriend_infos = config.get('girlfriend_infos')
        for girlfriend in girlfriend_infos:
            girlfriend.get('wechat_name').strip()
            # 根据城市名称获取城市编号。查看支持的城市为：http://cdn.sojson.com/_city.json
            city_name = girlfriend.get('city_name').strip()
            city_code = city_dict.city_dict.get(city_name)
            if not city_code:  # 如果没有城市code,跳过此用户。
                print('您输入的城市『{}』无法收取到天气信息。'.format(city_name))
                break
            girlfriend['city_code'] = city_code
            girlfriend_list.append(girlfriend)
            print_msg = (
                '女朋友的微信昵称：{wechat_name}\n\t女友所在城市名称：{city_name}\n\t'
                '在一起的第一天日期：{start_date}\n\t最后一句为：{sweet_words}\n'.format(**girlfriend))
            init_msg += print_msg

        print('*' * 50)
        print(init_msg)

        hour, minute = [int(x) for x in alarm_timed.split(':')]
        return girlfriend_list, hour, minute, dictum_channel, is_turing

    @staticmethod
    def is_online(auto_login=False):
        """
        判断是否还在线。
        :param auto_login: bool,如果掉线了则自动登录(默认为 False)。
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

        if _online():
            return True
        # 仅仅判断是否在线。
        if not auto_login:
            return _online()

        # 登陆，尝试 5 次。
        for _ in range(5):
            # 命令行显示登录二维码。
            # 如果需要切换微信，删除 hotReload=True
            if os.environ.get('MODE') == 'server':
                itchat.auto_login(enableCmdQR=2, hotReload=True)
            else:
                itchat.auto_login(hotReload=True)
            # if os.environ.get('MODE') == 'server':
            #     itchat.auto_login(enableCmdQR=2)
            # else:
            #     itchat.auto_login()
            if _online():
                print('登录成功')
                return True

        print('登录成功')
        return False

    def run(self):
        """
        主运行入口。
        :return:None
        """

        global reply_name_uuid_list
        # 自动登录
        if not self.is_online(auto_login=True):
            return
        for girlfriend in self.girlfriend_list:
            wechat_name = girlfriend.get('wechat_name')
            # 搜索用户名搜索用户，得到一个 用户列表 list
            friends = itchat.search_friends(name=wechat_name)
            if not friends:  # 如果用户列表为空，表示用户昵称填写有误。
                print('昵称『{}』有误。'.format(wechat_name))
                return
            name_uuid = friends[0].get('UserName')  # 取第一个用户的 uuid。
            girlfriend['name_uuid'] = name_uuid

            if name_uuid not in reply_name_uuid_list:
                reply_name_uuid_list.append(name_uuid)

        # 定时任务
        scheduler = BlockingScheduler()

        # 每天9：30左右给女朋友发送每日一句
        # scheduler.add_job(self.start_today_info, 'cron', hour=self.alarm_hour,
        #                   minute=self.alarm_minute, misfire_grace_time=GRACE_PERIOD)

        # 每隔 2 分钟发送一条数据用于测试。
        # scheduler.add_job(self.start_today_info, 'interval', seconds=120)

        if self.is_turing:
            def _itchatRun():
                itchat.run()

            print('已开启图灵自动回复...')
            thread = threading.Thread(target=_itchatRun, name='LoopThread')
            thread.start()
            scheduler.start()
            thread.join()
        else:
            scheduler.start()

    @itchat.msg_register([TEXT])
    def text_reply(msg):
        '''
        自动回复内容
        :return:
        '''
        try:
            # print(msg)
            uuid = msg.fromUserName
            if uuid in reply_name_uuid_list:
                receive_text = msg.text  # 好友发送来的消息
                # reply_text = receive_text * 3
                # 通过图灵 api 获取要回复的内容。
                reply_text = get_turing_msg(receive_text)
                time.sleep(2)
                if reply_text:  # 如内容不为空，回复消息
                    msg.user.send(reply_text)
                    print('{}发来信息：{}\n回复{}：{}'
                          .format(msg.user.nickName, receive_text, msg.user.nickName, reply_text))
                else:
                    print('{}发来信息：{}\t 自动回复失败'
                          .format(msg.user.nickName, receive_text))
        except Exception as e:
            print(str(e))

    def start_today_info(self, is_test=False):
        """
        每日定时开始处理。
        :param is_test:bool, 测试标志，当为True时，不发送微信信息，仅仅获取数据。
        :return: None.
        """
        print('*' * 50)
        print('获取相关信息...')

        if self.dictum_channel == 1:
            dictum_msg = self.get_dictum_info()
        elif self.dictum_channel == 2:
            dictum_msg = self.get_ciba_info()
        elif self.dictum_channel == 3:
            dictum_msg = self.get_lovelive_info()
        elif self.dictum_channel == 4:
            dictum_msg = self.get_hitokoto_info()
        else:
            dictum_msg = ''

        for girlfriend in self.girlfriend_list:
            city_code = girlfriend.get('city_code')
            start_date = girlfriend.get('start_date')
            sweet_words = girlfriend.get('sweet_words')
            # 获取天气信息，并整合数据。
            today_msg = self.get_weather_info(
                dictum_msg, city_code=city_code, start_date=start_date, sweet_words=sweet_words)
            name_uuid = girlfriend.get('name_uuid')
            wechat_name = girlfriend.get('wechat_name')
            print('给『{}』发送的内容是:\n{}'.format(wechat_name, today_msg))
            # 当为 is_test = True 时，不发送微信信息，仅仅获取数据
            if not is_test:
                if self.is_online(auto_login=True):  # 微信在线
                    # 发送微信消息
                    itchat.send(today_msg, toUserName=name_uuid)
                # 防止信息发送过快。
                time.sleep(5)

        print('发送成功...\n')

    @staticmethod
    def is_json(resp):
        """
        判断数据是否能被 Json 化。 True 能，False 否。
        :param resp: request.
        :return: bool, True 数据可 Json 化；False 不能 JOSN 化。
        """
        try:
            resp.json()
            return True
        except JSONDecodeError:
            return False

    def get_ciba_info(self):
        """
        从词霸中获取每日一句，带英文。
        :return:str ,返回每日一句（双语）
        """
        print('获取格言信息（双语）...')
        try:
            resp = requests.get('http://open.iciba.com/dsapi')
            if resp.status_code == 200 and self.is_json(resp):
                content_dict = resp.json()
                content = content_dict.get('content')
                note = content_dict.get('note')
                return '{}\n{}\n'.format(content, note)

            print('没有获取到格言数据。')
            return None
        except requests.exceptions.RequestException as exception:
            print(exception)
            return None
        return None

    def get_dictum_info(self):
        """
        获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
        :return: str， 一句格言或者短语。
        """
        print('获取格言信息...')
        user_url = 'http://wufazhuce.com/'

        resp = requests.get(user_url, headers=self.headers)
        if resp.status_code == 200:
            soup_texts = BeautifulSoup(resp.text, 'lxml')
            # 『one -个』 中的每日一句
            every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
            return every_msg + '\n'
        print('每日一句获取失败。')
        return None

    @staticmethod
    def get_lovelive_info():
        """
        从土味情话中获取每日一句。
        :return: str,土味情话。
        """
        print('获取土味情话...')
        try:
            resp = requests.get('https://api.lovelive.tools/api/SweetNothings')
            if resp.status_code == 200:
                return resp.text + '\n'
            print('土味情话获取失败。')
        except requests.exceptions.RequestException as exception:
            print(exception)
            return None
        return None

    @staticmethod
    def get_hitokoto_info():
        """
        从『一言』获取信息。(官网：https://hitokoto.cn/)
        :return: str,一言。
        """
        print('获取一言...')
        try:
            resp = requests.get('https://v1.hitokoto.cn/', params={'encode': 'text'})
            if resp.status_code == 200:
                return resp.text + '\n'
            print('一言获取失败。')
        except requests.exceptions.RequestException as exception:
            print(exception)
            return None
        return None

    def get_weather_info(self, dictum_msg, city_code, start_date, sweet_words):
        """
        获取天气信息。网址：https://www.sojson.com/blog/305.html .
        :param dictum_msg: str,发送给朋友的信息。
        :param city_code: str,城市对应编码。如：101030100
        :param start_date: str,恋爱第一天日期。如：2018-01-01
        :param sweet_words: str,来自谁的留言。如：来自你的朋友
        :return: str,需要发送的话。
        """
        print('获取天气信息...')
        weather_url = 'http://t.weather.sojson.com/api/weather/city/{}'.format(city_code)
        resp = requests.get(url=weather_url)
        if resp.status_code == 200 and self.is_json(resp) and resp.json().get('status') == 200:
            weather_dict = resp.json()
            # 今日天气
            today_weather = weather_dict.get('data').get('forecast')[0]
            # 今日日期
            today_time = (datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S')
                          .format(y='年', m='月', d='日'))
            # 今日天气注意事项
            notice = today_weather.get('notice')
            # 温度
            high = today_weather.get('high')
            high_c = high[high.find(' ') + 1:]
            low = today_weather.get('low')
            low_c = low[low.find(' ') + 1:]
            temperature = '温度 : {}/{}'.format(low_c, high_c)

            # 风
            wind_direction = today_weather.get('fx')
            wind_level = today_weather.get('fl')
            wind = '{} : {}'.format(wind_direction, wind_level)

            # 空气指数
            aqi = today_weather.get('aqi')
            aqi = '空气 : {}'.format(aqi)

            # 在一起，一共多少天了，如果没有设置初始日期，则不用处理
            if start_date:
                try:
                    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                    day_delta = (datetime.now() - start_datetime).days
                    delta_msg = '宝贝这是我们在一起的第 {} 天。\n'.format(day_delta)
                except ValueError:
                    delta_msg = ''
            else:
                delta_msg = ''

            today_msg = (
                '{today_time}\n{delta_msg}{notice}。\n{temperature}\n'
                '{wind}\n{aqi}\n{dictum_msg}{sweet_words}\n'.format(
                    today_time=today_time, delta_msg=delta_msg, notice=notice,
                    temperature=temperature, wind=wind, aqi=aqi,
                    dictum_msg=dictum_msg, sweet_words=sweet_words if sweet_words else ""))
            return today_msg


def get_turing_msg(text):
    """
    通过 图灵 api 获取对话
    :param text:
    :return:
    """
    url = "http://openapi.tuling123.com/openapi/api/v2"
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text
            }
        },
        "userInfo": {
            # 图灵机器人apiKey,需官网申请
            "apiKey": tuling_apikey,
            "userId": tuling_userid
        }
    }
    try:
        # print('发出消息:{}'.format(text))
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            # print(resp.text)
            conent = resp.json()
            if resp.json()['intent']['code'] not in TULING_ERROR_CODE_LIST:
                return_text = conent['results'][0]['values']['text']
                return return_text
            else:
                error_text = conent['results'][0]['values']['text']
                print('图灵机器人错误信息：{}'.format(error_text))
        print('图灵机器人发送失败')
        return None
    except Exception as e:
        print(e)
        return None
    return None


if __name__ == '__main__':
    # 直接运行
    # GFWeather().run()

    # 只查看获取数据，
    # GFWeather().start_today_info(True)

    # 测试获取词霸信息
    # ciba = GFWeather().get_ciba_info()
    # print(ciba)

    # 测试获取每日一句信息
    # dictum = GFWeather().get_dictum_info()
    # print(dictum)

    # 测试获取天气信息
    # wi = GFWeather().get_weather_info('好好学习，天天向上 \n', city_code='101030100',
    #                                   start_date='2018-01-01', sweet_words='美味的肉松')
    # print(wi)

    pass
