![python_vesion](https://img.shields.io/badge/Python-3.5%2B-green.svg)   [![itchat_vesion](https://img.shields.io/badge/Itchat-1.3.10-brightgreen.svg)](https://github.com/littlecodersh/ItChat)   [![codebeat badge](https://codebeat.co/badges/0953014f-dbd3-41f4-bacd-60018e7d5065)](https://codebeat.co/projects/github-com-sfyc23-everydaywechat-master)   [![MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/sfyc23/EverydayWechat/blob/master/LICENSE)               [![weibo](https://img.shields.io/badge/weibo-@sfyc23-red.svg)](https://www.weibo.com/sfyc23)



[EverydayWechat](https://github.com/sfyc23/EverydayWechat) 是基于 Python3 与 [Itchat](https://github.com/littlecodersh/ItChat) 的微信小工具。  
可以定时给朋友或者群聊发送每日天气、提醒、每日一句，也可以智能自动回复好友信息。  
操作简单，小白用户也可快速上手。

> 注意：如果给女朋友添加图灵机器人回复，请慎重考虑！！！！  
并不是你的每一个女朋友都能接受，你用机器人给他回复『暖心话』，安慰她。人工智能也有可能是一个智障机器人。想想如果机器人回复给你女朋友：『我们分手吧』。可能你们真的就分手了。虽然我会在心里默默的点个赞（单身狗的自白）
> 

## 功能说明

- 支持对多个微信好友自动回复。
- 定时给好友与群聊组发送提醒，内容包括（天气、格言、自定义的话）。

> 如果你没有好友可测试发送提醒，而且只有一个人也玩不了自动回复，怎么办呢（快哭了.jpg）。  
> 你可以把『文件传输助手』当成女朋友添加（你说的这个女朋友到底是不是你的双手.jpg）。这样一个号也可以进行测试了，发提醒给文件传输助手，跟文件传输助手智能聊天。


## 相关数据来源

### 天气信息：

- SOJSON：<https://www.sojson.com/blog/305.html>
- RollToolsApi：[获取特定城市今日天气](https://github.com/MZCretin/RollToolsApi#%E8%8E%B7%E5%8F%96%E7%89%B9%E5%AE%9A%E5%9F%8E%E5%B8%82%E4%BB%8A%E6%97%A5%E5%A4%A9%E6%B0%94)

### 每日一句：

- ONE ● 一个： <http://wufazhuce.com/>
- 金山词霸 ● 每日一句（双语）：<http://open.iciba.com/?c=api>
- 一言 ：<https://hitokoto.cn/>
- 土味情话： <https://www.v2ex.com/t/569853> (目前已失联)
- 民国情书 句子迷
- RollToolsApi: [随机获取笑话段子列表](https://github.com/MZCretin/RollToolsApi#%E9%9A%8F%E6%9C%BA%E8%8E%B7%E5%8F%96%E7%AC%91%E8%AF%9D%E6%AE%B5%E5%AD%90%E5%88%97%E8%A1%A8)

### 人工智能机器人

- 图灵机器人：<http://www.turingapi.com/>（需求实名制认证，并每天免费数量只有100条）
- 一个AI：<http://www.yige.ai/>（免费且无数量限制。可自定义回复、对话、场景。但高级功能使用比较复杂）
- 青云客智能聊天机器人：<http://api.qingyunke.com/>（无须申请，无数量限制，但有点智障，分手神器。分手神器，慎用）

计划再想加上幽默段子，养生之类的数据来源，欢迎提供相关网页与接口。

## 项目配置
目前项目所有的配置都是在 **[_config.yaml](https://github.com/sfyc23/EverydayWechat/blob/master/_config.yaml)** 文件中。  
配置文件请严格遵循 yaml 语法格式，yaml 学习地址:  
<https://ansible-tran.readthedocs.io/en/latest/docs/YAMLSyntax.html>    
<http://einverne.github.io/post/2015/08/yaml.html>

### 配置自动回复机器人。

#### 1. 开启自动回复
将 **is_auto_relay** 设置为：True。

#### 2.选择渠道
```
机器人渠道（1: 图灵机器人，2: 一个AI ,3 : 青云客)
bot_channel: 3
```

> 默认为青云客，但请注意这个比较智障。。

#### 3. 配置图灵机器人
如果有需要。  
打开图灵机器人官网：[http://www.turingapi.com](http://www.turingapi.com/) 进行注册。  
创建机器人，得到 apikey。  
将填入到 **_config.yaml** 文件中的：
```
turing_conf:
  apiKey: '你所获取apikey'
```
> 图灵机器人必须认证后才能使用，免费版用户，每天可使用 100 条信息，且用且珍惜。

#### 4. 配置「一个AI」
打开图灵机器人官网：[http://www.yige.ai](http://www.yige.ai) 进行注册。  
创建应用，得到「API密钥」中的 「客户端访问令牌」
将填入到 **_config.yaml** 文件中的：
```
yigeai_conf:
  client_token: '客户访问令牌'
```


#### 5. 指定自动回复的好友名单

在 **auto_reply_names** 填入需要自动回复的好友名单。如下：

```
# 指定自动回复的好友名单。
auto_reply_names:
  - '好友1'
  - '好友2'
```

关于自动回复，目前可以公开的情报：
1. 只能自动回复文字类消息；
3. 群消息自动回复还未现实（待完成）；
4. 如果消息发送太频繁，微信会限制登录网页端登录。放心，并不会封号；
5. 并不是对所有人自动回复，只是回复 **auto_reply_names** 中的人；
6. 好友里可以填入名称『文件传输助手』，这样你就可以在文件传输助手，发送消息，查看自动回复消息效果。

### 配置定时提醒
#### 1.开启并设置提醒时间

* 将 **is_alarm** 设置成 **True**。（当为 False 时，则关闭定时）
* **alarm_time** 设置成需要提醒的时间。之后如果微信没有断线，即每天这个的时间会定时发送提醒。

如果需要快速体验，可将 **alarm_timed** 当前系统时间之后的几分钟。例如当前时间为 11:35，并设置 5 分钟后发送提醒，如下面示例：

```
alarm_info:
  is_alarm: True
  #定时发送时间
  alarm_timed: '11:40'
```
这样 5 分钟则会发送提醒。

#### 2.填写需要发送的好友信息

填写好友信息，例如：
```
girlfriend_infos:
  #  如果你有多个好友需要发送，则参照这个样式，复制即可
  - wechat_name: '宝宝'
    group_name: 'EverydayWechat 交流群'
    city_name: '朝阳区'
    dictum_channel : 4
    start_date: '2011-11-11'
    sweet_words: '来自最爱你的我。'
```

相关参数说明：

| 名称 | 示例       | 必填 | 说明 |
| -------- | -------------- | ---------- |---------- |
| wechat_name | '老婆' | 必填 |好友名：需要发送的人的微信昵称或者备注名（不能输入微信号）|
| group_name | '交流群' | 必填 |群聊名称，必须要把需要的群聊保存到通讯录。|
| city_name | '成都' | 可空| 城市名：女友所在城市，用于发送天气。 |
| dictum_channel | 2 |可空|格言渠道（1 : ONE●一个，2 : 词霸（双语），4 : 一言，5：笑话)|
| start_date | '2017-10-10' | 可空 |相识日期：计算到当天的天数 。|
| sweet_words |'来自你俊美的老公' | 可空 |甜密的后缀。（钢铁直男的直描）|

wechat_name，group_name 至少要有一个。

>Tips：可以把 **wechat_name**  填入『**文件传输助手**』，这样，提醒会发送到自己微信里的 **文件传输助手** 中。在不打扰别人的情况下，方便快速查看效果。

一例提醒：

    Without you, today's emotions would be the scurf of yesterday's.如果没有你，如此的良辰美景让我去向何人诉说？  
    2019-06-13 星期四 多云 北风 <3级 高温 29.0℃ 低温 22.0℃ 阴晴之间，谨防紫外线侵扰  
    宝贝这是我们在一起的第 611 天。  
    来自最爱你的我。

本项目在以下环境以测试通过：

| 系统名称 | 系统版本       | Python版本 |
| -------- | -------------- | ---------- |
| Windows  | Windows 10 x 64 | 3.6.5      |


## 安装
首先，把 Python3 安装好，并配置好环境，个人建议新手安装 anaconda，具体安装教程，可自行谷歌搜索~

直接下载此项目或 clone 项目到本地。  

使用 pip 安装依赖:

```
pip3 install -r requirements.txt
# pip install -r requirements.txt
```



## 运行：


在本地 cmd 中跳转项目目录下，运行：
```
python run.py
```

第一次运行会跳出二维码，扫码登录。如输出日志中打印成：『登录成功』，则表示运行成功。 
登录成功后一段时间内再运行，微信会保持登录状态，不需要再扫码。  
如果需要切换用户，则在 *_config.yaml* 文件中，修改 *is_forced_switch* 的属性为 True。

## 示例截图：

![日志](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613171703.png)

![自动回复](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613162524.png)

## 提 [issues](https://github.com/sfyc23/EverydayWechat/issues) & 加群提问的建议。

- 当你拋出一个技术问题时，最终是否能得到有用的回答，往往取决于你所提问和追问的方式。推荐阅读：[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md)。
- **检查是否是最新的代码，检查是否是 Python3.5+，检查依赖有没有安装完整**。
- 先检查微信是否可登录 [微信网页版](https://wx.qq.com/)，如网页端不能用，此项目也不能用。
- 请更新你的 [itchat](https://github.com/littlecodersh/ItChat) 至最新版本 **1.3.10** 。查看 itchat 版本 **print(itchat.__version__ ）**。
- 与微信相关的问题可以先去 itchat [issues](https://github.com/littlecodersh/ItChat/issues)， 查看是否有相似问题。
- 微信名只能是昵称或者备注名，不能输入微信号。
- 对群聊操作时，必须要把需要的群聊保存到通讯录。
- 如果有新的思路和建议也欢迎提交。


## Credits 致谢

本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。

- [wechatBot](https://github.com/gengchen528/wechatBot) —— 微信每日说，每日自动发送微信消息（Node + Wechaty）。  
- [NodeMail](https://github.com/Vincedream/NodeMail) —— 用 Node 写一个爬虫脚本每天定时给女朋友发一封暖心邮件。  
- [wechat-assistant](https://github.com/gengchen528/wechat-assistant) —— koa+wechaty实现的微信个人秘书，把你闲置的微信号利用起来做个个人秘书。
- <https://github.com/likaixiang/EverydayWechat>
- <https://github.com/0xHJK/music-dl>

## LICENSE
[MIT License](https://github.com/sfyc23/EverydayWechat/blob/master/LICENSE)

## 交流群

加我微信：[sfyc1314](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190614125724.png)，备注：Github。我拉你入群。
 ![我的微信](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190614125724.png)
 
