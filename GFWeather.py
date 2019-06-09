import requests
from datetime import datetime
from bs4 import BeautifulSoup
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import city_dict
import yaml


class gfweather:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    dictum_channel_name = {1: 'ONE●一个', 2: '词霸(每日英语)', 3: '土味情话'}

    def __init__(self):
        self.girlfriend_list, self.alarm_hour, self.alarm_minute, self.dictum_channel = self.get_init_data()

    def get_init_data(self):
        '''
        初始化基础数据
        :return:
        '''
        with open('_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        alarm_timed = config.get('alarm_timed').strip()
        init_msg = f"每天定时发送时间：{alarm_timed}\n"

        dictum_channel = config.get('dictum_channel', -1)
        init_msg += f"格言获取渠道：{self.dictum_channel_name.get(dictum_channel, '无')}\n"

        girlfriend_list = []
        girlfriend_infos = config.get('girlfriend_infos')
        for girlfriend in girlfriend_infos:
            girlfriend.get('wechat_name').strip()
            # 根据城市名称获取城市编号，用于查询天气。查看支持的城市为：http://cdn.sojson.com/_city.json
            city_name = girlfriend.get('city_name').strip()
            city_code = city_dict.city_dict.get(city_name)
            if not city_code:
                print('您输入的城市无法收取到天气信息')
                break
            girlfriend['city_code'] = city_code
            girlfriend_list.append(girlfriend)

            print_msg = f"女朋友的微信昵称：{girlfriend.get('wechat_name')}\n\t女友所在城市名称：{girlfriend.get('city_name')}\n\t" \
                f"在一起的第一天日期：{girlfriend.get('start_date')}\n\t最后一句为：{girlfriend.get('sweet_words')}\n"
            init_msg += print_msg

        print(u"*" * 50)
        print(init_msg)

        hour, minute = [int(x) for x in alarm_timed.split(':')]
        return girlfriend_list, hour, minute, dictum_channel

    def is_online(self, auto_login=False):
        '''
        判断是否还在线,
        :param auto_login:True,如果掉线了则自动登录。
        :return: True ，还在线，False 不在线了
        '''

        def online():
            '''
            通过获取好友信息，判断用户是否还在线
            :return: True ，还在线，False 不在线了
            '''
            try:
                if itchat.search_friends():
                    return True
            except:
                return False
            return True

        if online():
            return True
        # 仅仅判断是否在线
        if not auto_login:
            return online()

        # 登陆，尝试 5 次
        for _ in range(5):
            # 命令行显示登录二维码
            # itchat.auto_login(enableCmdQR=True)
            itchat.auto_login()
            if online():
                print('登录成功')
                return True
        else:
            print('登录成功')
            return False

    def run(self):
        '''
        主运行入口
        :return:None
        '''
        # 自动登录
        if not self.is_online(auto_login=True):
            return
        for girlfriend in self.girlfriend_list:
            wechat_name = girlfriend.get('wechat_name')
            friends = itchat.search_friends(name=wechat_name)
            if not friends:
                print('昵称错误')
                return
            name_uuid = friends[0].get('UserName')
            girlfriend['name_uuid'] = name_uuid

        # 定时任务
        scheduler = BlockingScheduler()
        # 每天9：30左右给女朋友发送每日一句
        scheduler.add_job(self.start_today_info, 'cron', hour=self.alarm_hour, minute=self.alarm_minute)
        # 每隔2分钟发送一条数据用于测试。
        # scheduler.add_job(self.start_today_info, 'interval', seconds=30)
        scheduler.start()

    def start_today_info(self, is_test=False):

        '''
        每日定时开始处理。
        :param is_test: 测试标志，当为True时，不发送微信信息，仅仅获取数据。
        :return:
        '''
        print("*" * 50)
        print('获取相关信息...')

        if self.dictum_channel == 1:
            dictum_msg = self.get_dictum_info()
        elif self.dictum_channel == 2:
            dictum_msg = self.get_ciba_info()
        elif self.dictum_channel == 3:
            dictum_msg = self.get_lovelive_info()
        else:
            dictum_msg = ''

        for girlfriend in self.girlfriend_list:
            city_code = girlfriend.get('city_code')
            start_date = girlfriend.get('start_date')
            sweet_words = girlfriend.get('sweet_words')
            today_msg = self.get_weather_info(dictum_msg, city_code=city_code, start_date=start_date,
                                              sweet_words=sweet_words)
            name_uuid = girlfriend.get('name_uuid')
            wechat_name = girlfriend.get('wechat_name')
            print(f'给『{wechat_name}』发送的内容是:\n{today_msg}')

            if not is_test:
                if self.is_online(auto_login=True):
                    itchat.send(today_msg, toUserName=name_uuid)
                # 防止信息发送过快。
                time.sleep(5)

        print('发送成功..\n')

    def isJson(self, resp):
        '''
        判断数据是否能被 Json 化。 True 能，False 否。
        :param resp:
        :return:
        '''
        try:
            resp.json()
            return True
        except:
            return False

    def get_ciba_info(self):
        '''
        从词霸中获取每日一句，带英文。
        :return:
        '''
        resp = requests.get('http://open.iciba.com/dsapi')
        if resp.status_code == 200 and self.isJson(resp):
            conentJson = resp.json()
            content = conentJson.get('content')
            note = conentJson.get('note')
            # print(f"{content}\n{note}")
            return f"{content}\n{note}\n"
        else:
            print("没有获取到数据")
            return None

    def get_dictum_info(self):
        '''
        获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
        :return: str 一句格言或者短语
        '''
        print('获取格言信息..')
        user_url = 'http://wufazhuce.com/'
        resp = requests.get(user_url, headers=self.headers)
        soup_texts = BeautifulSoup(resp.text, 'lxml')
        # 『one -个』 中的每日一句
        every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
        return every_msg + "\n"

    def get_lovelive_info(self):
        '''
        从土味情话中获取每日一句。
        '''
        resp = requests.get("https://api.lovelive.tools/api/SweetNothings")
        return resp.text + "\n"

    def get_weather_info(self, dictum_msg='', city_code='101030100', start_date='2018-01-01', sweet_words='来自最爱你的我'):
        '''
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :param dictum_msg: 发送给朋友的信息
        :param city_code: 城市对应编码
        :param start_date: 恋爱第一天日期
        :param sweet_words: 来自谁的留言
        :return: 需要发送的话。
        '''
        print('获取天气信息..')
        weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'
        resp = requests.get(url=weather_url)
        if resp.status_code == 200 and self.isJson(resp) and resp.json().get('status') == 200:
            weatherJson = resp.json()
            # 今日天气
            today_weather = weatherJson.get('data').get('forecast')[1]
            # 今日日期
            today_time = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')
            # 今日天气注意事项
            notice = today_weather.get('notice')
            # 温度
            high = today_weather.get('high')
            high_c = high[high.find(' ') + 1:]
            low = today_weather.get('low')
            low_c = low[low.find(' ') + 1:]
            temperature = f"温度 : {low_c}/{high_c}"

            # 风
            fx = today_weather.get('fx')
            fl = today_weather.get('fl')
            wind = f"{fx} : {fl}"

            # 空气指数
            aqi = today_weather.get('aqi')
            aqi = f"空气 : {aqi}"

            # 在一起，一共多少天了，如果没有设置初始日期，则不用处理
            if start_date:
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
                day_delta = (datetime.now() - start_datetime).days
                delta_msg = f'宝贝这是我们在一起的第 {day_delta} 天。\n'
            else:
                delta_msg = ''

            today_msg = f'{today_time}\n{delta_msg}{notice}。\n{temperature}\n{wind}\n{aqi}\n{dictum_msg}{sweet_words if sweet_words else ""}\n'
            return today_msg


if __name__ == '__main__':

    # 直接运行
    # gfweather().run()

    # 只查看获取数据，
    # gfweather().start_today_info(True)

    # 测试获取词霸信息
    # ciba = gfweather().get_ciba_info()
    # print(ciba)

    # 测试获取每日一句信息
    # dictum = gfweather().get_dictum_info()
    # print(dictum)

    # 测试获取天气信息
    # wi = gfweather().get_weather_info('丽华\n')
    # print(wi)
    pass
