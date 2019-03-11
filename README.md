# 用 Python + itchat 写一个爬虫脚本每天定时给女朋友发微信暖心话

##项目介绍：

### 灵感来源

在掘金看到了一篇《[用Node+wechaty写一个爬虫脚本每天定时给女(男)朋友发微信暖心话][1]》后，我就想为什么不用 Python 去实现这个功能呢。 Just to IT，说做就做。  
这文章的结构也是参考上面这位朋友的。


### 项目地址：
Github: [https://github.com/sfyc23/EverydayWechat](https://github.com/sfyc23/EverydayWechat)。

### 使用库
- [itchat][2] - 微信个人号接口
- [requests][3] - 网络请求库
- [beautifulsoup4][4] - 解析网页
- [APScheduler][5] - 定时任务

### 功能
定时给女朋友发送每日天气、提醒、每日一句。

### 数据来源
- 每日一句和上面的大佬一样也是来自 [ONE·一个][6]
- 天气信息来自 [SOJSON][7] 


### 实现效果
![命令行信息](http://vlog.sfyc23.xyz/wechat_everyday/20190312010620.png)  
![微信截图](http://vlog.sfyc23.xyz/wechat_everyday/20190312010621.png)

## 代码说明

### 目录结构
![](http://vlog.sfyc23.xyz/wechat_everyday/20190312011740.png)  
- city_dict.py ：城市对应编码字典
- config.yaml ：设置定时时间，女友微信名称等参数
- GFWeather.py：核心代码
- requirements.txt：需要安装的库
- run.py：项目运行类

### 核心代码
GFWeather.py
```
class gfweather:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    # 女朋友的用户id
    bf_wechat_name_uuid = ''
    def __init__(self):
        self.city_code, self.start_datetime, self.bf_wechat_name, self.alarm_hour, self.alarm_minute = self.get_init_data()

    def get_init_data(self):
        '''
        初始化基础数据
        :return:
        '''
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.load(f)
        city_name = config.get('city_name').strip()
        start_date = config.get('start_date').strip()
        wechat_name = config.get('wechat_name').strip()
        alarm_timed = config.get('alarm_timed').strip()

        init_msg = f"每天定时发送时间：{alarm_timed}\n女友所在城市名称：{city_name}\n女朋友的微信昵称：{wechat_name}\n在一起的第一天日期：{start_date}"
        print(u"*" * 50)
        print(init_msg)

        # 根据城市名称获取城市编号，用于查询天气。查看支持的城市为：http://cdn.sojson.com/_city.json
        city_code = city_dict.city_dict.get(city_name)
        if not city_code:
            print('您输出城市无法收取到天气信息')
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        hour, minute = [int(x) for x in alarm_timed.split(':')]
        # print(hour, minute)
        return city_code, start_datetime, wechat_name, hour, minute

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
            return False

    def run(self):

        # 自动登录
        if not self.is_online(auto_login=True):
            return

        # 定时任务
        scheduler = BlockingScheduler()
        # 每天9：30左右给女朋友发送每日一句
        scheduler.add_job(self.start_today_info, 'cron', hour=self.alarm_hour, minute=self.alarm_minute)
        scheduler.start()

    def start_today_info(self):

        print("*" * 50)
        print('获取相关信息...')
        dictum_msg = self.get_dictum_info()
        today_msg = self.get_weather_info(dictum_msg)

        print(f'要发送的内容:\n{today_msg}')
        if self.is_online(auto_login=True):
            # 获取好友username
            if not self.bf_wechat_name_uuid:
                friends = itchat.search_friends(name=self.bf_wechat_name)
                if not friends:
                    print('昵称错误')
                    return
                self.bf_wechat_name_uuid = friends[0].get('UserName')
            itchat.send(today_msg, toUserName=self.bf_wechat_name_uuid)
        print('发送成功..\n')

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
        return every_msg

    def get_weather_info(self, dictum_msg=''):
        '''
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :param dictum_msg: 发送给朋友的信息
        :return:
        '''
        print('获取天气信息..')
        weather_url = f'http://t.weather.sojson.com/api/weather/city/{self.city_code}'
        resp = requests.get(url=weather_url)
        if resp.status_code == 200 and resp.json().get('status') == 200:
            weatherJson = resp.json()
            # 今日天气
            today_weather = weatherJson.get('data').get('forecast')[1]
            locale.setlocale(locale.LC_CTYPE, 'chinese')
            today_time = datetime.now().strftime('"%Y年%m月%d日 %H:%M:%S"')

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
            day_delta = (datetime.now() - self.start_datetime).days
            delta_msg = f'宝贝这是我们在一起的第 {day_delta} 天'

            today_msg = f'{today_time}\n{delta_msg}。\n{notice}\n{temperature}\n{wind}\n{aqi}\n{dictum_msg}\n来自最爱你的我。'
            return today_msg
```

## 项目运行

### 安装依赖

使用 pip install -r requirements.txt 安装所有依赖

### 参数配置
config.yaml
```
#每天定时发送的时间点，如：8：30
alarm_timed: '9:30'
# 女友所在城市名称
city_name: '桂林'
# 你女朋友的微信名称
wechat_name: '古典'
# 从那天开始勾搭的
start_date: '2017-11-11'
```

### 开始运行
```
python run.py
```

## 最后
项目地址：[https://github.com/sfyc23/EverydayWechat](https://github.com/sfyc23/EverydayWechat)  
写完后才发现，我并没有女朋友啊！


  [1]: https://juejin.im/post/5c77c6bef265da2de6611cff
  [2]: https://github.com/littlecodersh/ItChat
  [3]: http://docs.python-requests.org/en/master/
  [4]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#
  [5]: https://apscheduler.readthedocs.io/en/latest/
  [6]: http://wufazhuce.com/
  [7]: https://www.sojson.com/blog/305.html