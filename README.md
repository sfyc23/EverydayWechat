![python_vesion](https://img.shields.io/badge/Python%20-%3E%3D%203.5-green.svg)  
# 用 Python + itchat 写一个爬虫脚本每天定时给多个女友发给微信暖心话

## 待优化功能：

> * [ ]  正在重构代码中。。。
> * [ ]  更友好的 DEBUG 和文档，方便第一次跑通程序。
> * [ ]  断线提醒。
> * [ ]  给女友群发消息。



2019-6-12 已添加图灵机器人实现自动回复。

---
## 项目介绍：

### 开发环境

    Python >= 3.5

### 灵感来源

在掘金看到了一篇《[用Node+wechaty写一个爬虫脚本每天定时给女(男)朋友发微信暖心话](https://juejin.im/post/5c77c6bef265da2de6611cff)》后，我就想为什么不用 Python 去实现这个功能呢。 JUST DO IT，说做就做。  
这文章的结构也是参考上面这位朋友的。  
本来只是写单人的，不过有些优（作）秀（死）的人表示女朋友不止一个。现已支持添加多人信息。

### 项目地址：
Github: [https://github.com/sfyc23/EverydayWechat](https://github.com/sfyc23/EverydayWechat)。


### 使用库
- [itchat](https://github.com/littlecodersh/ItChat) - 微信个人号接口
- [requests](http://docs.python-requests.org/en/master/) - 网络请求库
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#) - 解析网页
- [APScheduler](https://apscheduler.readthedocs.io/en/latest/) - 定时任务

### 功能
定时给女朋友发送每日天气、提醒、每日一句。

### 数据来源
- 每日一句和上面的大佬一样也是来自 [ONE●一个](http://wufazhuce.com/)
- 金山词霸 ● 每日一句（英文加中文）：[iciba](http://open.iciba.com/?c=api)
- 一言 ：[hitokoto](https://hitokoto.cn/)
- 土味情话： [渣男在线](https://www.v2ex.com/t/569853)(目前失效。)
- 天气信息来自： [SOJSON](https://www.sojson.com/blog/305.html) 

### 实现效果
![命令行信息](http://vlog.sfyc23.xyz/wechat_everyday/20190312010620.png)  
![微信截图](http://vlog.sfyc23.xyz/wechat_everyday/20190312010621.png)

图灵自动回复机器人：

![自动回复机器人](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190612173126.jpg)

这简直就是分手神器！
## 代码说明

### 目录结构
![](http://vlog.sfyc23.xyz/wechat_everyday/20190312011740.png)  

- city_dict.py ：城市对应编码字典
- config.yaml ：设置定时时间，女友微信名称等参数
- GFWeather.py：核心代码
- requirements.txt：需要安装的库
- run.py：项目运行类

### 核心代码

#### 1. 定时任务。
每天 9：30 给女朋友们开始给女朋友发送内容。
```
# 定时任务
scheduler = BlockingScheduler()
# 每天9：30给女朋友发送每日一句
# scheduler.add_job(start_today_info, 'cron', hour=9, minute=30)
scheduler.start()
```
*start_today_info* 是方法处理类。

#### 2. 获取每日一句。
数据来源 1： [ONE●一个](http://wufazhuce.com/)
```
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
```
数据来源 2： [金山词霸 ● 每日一句](http://open.iciba.com/?c=api)  

有英文和中文翻译，例如：
> When you finally get your own happiness, you will understand the
> previous sadness is a kind of treasure, which makes you better to hold
> and cherish the people you love.  
> 等你获得真正属于你的幸福之后，你就会明白一起的伤痛其实是一种财富，它让你学会更好地去把握和珍惜你爱的人。

代码实现 ：
```
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
```

数据来源 3： [土味情话](https://api.lovelive.tools/api/SweetNothings)（感谢 [tomatoF](https://github.com/tomatoF)、[QSCTech-Sange](https://github.com/QSCTech-Sange))（已失效）

```
def get_lovelive_info(self):
    '''
    从土味情话中获取每日一句。
    '''
    resp = requests.get("https://api.lovelive.tools/api/SweetNothings")
    if resp.status_code == 200:
        return resp.text + "\n"
    else:
        print('每日一句获取失败')
        return None
```

数据来源 4： [一言](https://v1.hitokoto.cn/)

```
def get_hitokoto_info():
    try:
        resp = requests.get('https://v1.hitokoto.cn/', params={'encode': 'text'})
        if resp.status_code == 200:
            return resp.text + '\n'
        print('一言获取失败。')
    except requests.exceptions.RequestException as exception:
        print(exception)
        return None
    return None
```

#### 3. 获取今日天气 。
天气数据来源：[SOJSON](https://www.sojson.com/blog/305.html)

```
def get_weather_info(self, city_code=''）：
    weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'
    resp = requests.get(url=weather_url)
    if resp.status_code == 200 and resp.json().get('status') == 200:
        weatherJson = resp.json()
        # 今日天气
        today_weather = weatherJson.get('data').get('forecast')[1]
```
city_code 城市对应 id。
[http://cdn.sojson.com/_city.json](http://cdn.sojson.com/_city.json)

#### 4. 登录微信并发送内容。
```
itchat.auto_login()
itchat.send(today_msg, toUserName=name_uuid)
```



## 项目配置

### 配置图灵机器人自动回复

1. 打开图灵机器人官网：[http://www.turingapi.com](http://www.turingapi.com/) 进行注册。
2. 通过认证后，创建机器人,得到 apikey，userid。
3. 将获取到的 apiKey，userId 填入到 **_config.yaml** 文件中：
```
turing_conf:
  # 是否开启自动回复,只可选 False && True
  is_turing: True
  apiKey: ''
  userId: ''
```


目前可以公开的情报：
1. 只能自动回复文字类消息；
2. 免费版用户，每天可使用 100 条信息，且用且珍惜；
3. 群消息自动回复还未现实。（待完成）；
4. 如果消息发送太频繁，微信会限制登录网页端登录。放心，并不会封号；
5. 并不是对所有人自动回复，只是回复 girlfriend_infos 中的人。

### 安装依赖

使用 pip install -r requirements.txt 安装所有依赖

### 参数配置
config.yaml
```
# 定时时间
alarm_timed: '9:30'

# 格言渠道
# 1 : ONE●一个
# 2 : 词霸（每日英语,双语）
# 3 : 土味情话
# 4 : 一言
dictum_channel: 2

girlfriend_infos:
  -
    #女友微信昵称
    wechat_name: '古典'
    #女友所在桂林
    city_name: '桂林'
    # 从那天开始勾搭的（可空）
    start_date: '2017-11-11'
    # 短句的最后留言（可空）
    sweet_words: '来自最爱你的我。'

  #如果有你多个人需要发送，则参照这个样式，复制即可
  -
    wechat_name: '陈老师'
    city_name: '朝阳区'
    start_date: '2018-11-11'
    sweet_words: '来自你俊美的老公。'
```

## 项目运行

建议使用微信小号。

### 1.直接运行
```
python run.py
```

### 2.使用 Screen 开始运行
```
screen -S '项目所在地址'
python run.py
#Ctrl+A+D 退出 Screen 窗口
```

### 3.使用 Docker
```
sudo docker build -t everydaywechat .
sudo docker run --name '项目所在地址'
# 扫码登陆
#Ctrl+P+Q 退出容器
```

## 最后
项目地址：[https://github.com/sfyc23/EverydayWechat](https://github.com/sfyc23/EverydayWechat)  。
写完后才发现，我并没有女朋友啊！



## Credits 致谢

本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。

- [wechatBot](https://github.com/gengchen528/wechatBot) —— 微信每日说，每日自动发送微信消息（Node + Wechaty）。  
- [NodeMail](https://github.com/Vincedream/NodeMail) —— 用 Node 写一个爬虫脚本每天定时给女朋友发一封暖心邮件。  
- [wechat-assistant](https://github.com/gengchen528/wechat-assistant) —— koa+wechaty实现的微信个人秘书，把你闲置的微信号利用起来做个个人秘书。
- <https://github.com/likaixiang/EverydayWechat>

## LICENSE
[MIT License](https://github.com/sfyc23/EverydayWechat/blob/master/LICENSE)