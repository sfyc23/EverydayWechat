![python_vesion](https://img.shields.io/badge/Python-3.5%2B-green.svg)   [![itchat_vesion](https://img.shields.io/badge/Itchat-1.3.10-brightgreen.svg)](https://github.com/littlecodersh/ItChat)   [![codebeat badge](https://codebeat.co/badges/0953014f-dbd3-41f4-bacd-60018e7d5065)](https://codebeat.co/projects/github-com-sfyc23-everydaywechat-master)   [![Codacy Badge](https://api.codacy.com/project/badge/Grade/a278078ba9a14e22bd86740b0807a78e)](https://www.codacy.com/app/sfyc23/EverydayWechat?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sfyc23/EverydayWechat&amp;utm_campaign=Badge_Grade)   [![MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/sfyc23/EverydayWechat/blob/master/LICENSE)               [![weibo](https://img.shields.io/badge/weibo-@sfyc23-red.svg)](https://www.weibo.com/sfyc23)  [![GitHub issues](https://img.shields.io/github/issues/sfyc23/EverydayWechat.svg)](https://github.com/sfyc23/EverydayWechat/issues)  [![GitHub contributors](https://img.shields.io/github/contributors/sfyc23/EverydayWechat.svg)](https://github.com/sfyc23/EverydayWechat/graphs/contributors)  [![微信群](http://vlog.sfyc23.xyz/wechat_everyday/wxgroup_logo.png?imageView2/0/w/60/h/20)](#微信交流群)  
 
[EverydayWechat](https://github.com/sfyc23/EverydayWechat) 是基于 Python3 与 [Itchat](https://github.com/littlecodersh/ItChat) 的微信小工具。    
可以定时给朋友或者群聊发送每日天气、提醒、每日一句，也可以智能自动回复好友信息。    
操作简单，小白用户也可快速上手。  

[版本更新日志](https://github.com/sfyc23/EverydayWechat/blob/master/hostory.md)

**禁止将本工具用于商业用途**，如产生法律纠纷与本人无关。  

> 注意：如果给女朋友添加图灵机器人回复，请慎重考虑！！！！  
并不是你的每一个女朋友都能接受，你用机器人给他回复『暖心话』，安慰她。人工智能也有可能是一个智障机器人。想想如果机器人回复给你女朋友：『我们分手吧』。可能你们真的就分手了。虽然我会在心里默默的点个赞（单身狗的自白）
> 

 [![GitHub stars](https://img.shields.io/github/stars/sfyc23/EverydayWechat.svg?style=social)](https://github.com/sfyc23/EverydayWechat/stargazers)     [![GitHub forks](https://img.shields.io/github/forks/sfyc23/EverydayWechat.svg?style=social)](https://github.com/sfyc23/EverydayWechat/network/members)  `请点击页面顶部靠右 star 与 fork`  

## 功能说明

-  支持对多个微信好友自动回复。  
-  定时给好友与群聊组发送提醒，内容包括（天气、格言、自定义的话）。  

> 如果你没有好友可测试发送提醒，而且只有一个人也玩不了自动回复，怎么办呢（快哭了.jpg）。  
> 你可以把『文件传输助手』当成女朋友添加（你说的这个女朋友到底是不是你的双手.jpg）。这样一个号也可以进行测试了，发提醒给文件传输助手，跟文件传输助手智能聊天。

## 相关数据来源

### 天气信息：

-  SOJSON：<https://www.sojson.com/blog/305.html>    
-  RollToolsApi：[获取特定城市今日天气](https://github.com/MZCretin/RollToolsApi#%E8%8E%B7%E5%8F%96%E7%89%B9%E5%AE%9A%E5%9F%8E%E5%B8%82%E4%BB%8A%E6%97%A5%E5%A4%A9%E6%B0%94)    

### 每日一句：

-  ONE ● 一个： <http://wufazhuce.com/>  
-  金山词霸 ● 每日一句（双语）：<http://open.iciba.com/?c=api>  
-  一言 ：<https://hitokoto.cn/>  
-  土味情话： <https://www.v2ex.com/t/569853> (土)  
-  句子迷-民国情书: <https://www.juzimi.com/> (高雅)  
-  RollToolsApi: [随机获取笑话段子列表](https://github.com/MZCretin/RollToolsApi#%E9%9A%8F%E6%9C%BA%E8%8E%B7%E5%8F%96%E7%AC%91%E8%AF%9D%E6%AE%B5%E5%AD%90%E5%88%97%E8%A1%A8)      
-  彩虹屁: <https://chp.shadiao.app>  

### 人工智能机器人

-  图灵机器人：<http://www.turingapi.com/>（需求实名制认证，并每天免费数量只有100条）  
-  一个AI：<http://www.yige.ai/>（免费且无数量限制。可自定义回复、对话、场景。但高级功能使用比较复杂。但已长时间没人维护）    
-  青云客智能聊天机器人：<http://api.qingyunke.com/>（无须申请，无数量限制，但有点智障，分手神器。分手神器，慎用）  
-  智能闲聊（腾讯）<https://ai.qq.com/product/nlpchat.shtml> ( 申请使用，免费且无限量。大厂靠谱。)  
-  天行机器人 <https://www.tianapi.com/apiview/47> (认证后有7万条免费使用。之后收费：1万条/1块钱)  
-  海知智能 <https://ruyi.ai/> （功能很强大，不仅仅用于聊天。需申请 key，免费） 

### 星座运势
-  星座屋 ：<https://www.xzw.com/> (基于爬虫获取数据)  

### 万年历
-  RollToolsApi ：[指定日期的节假日及万年历信息](https://github.com/MZCretin/RollToolsApi#指定日期的节假日及万年历信息)    
-  SOJSON ：<https://www.sojson.com/api/lunar.html>  

## 项目配置
目前项目所有的配置都是在 **[_config.yaml](https://github.com/sfyc23/EverydayWechat/blob/master/_config.yaml)** 文件中。    
配置文件请严格遵循 yaml 语法格式，yaml 学习地址:  
<https://ansible-tran.readthedocs.io/en/latest/docs/YAMLSyntax.html>    
<http://einverne.github.io/post/2015/08/yaml.html>

### 配置自动回复机器人。

#### 1. 开启自动回复

-  将 **is_auto_relay** 设置为：True。  

#### 2.选择渠道
```
机器人渠道（1: 图灵机器人，2: 一个AI ,3 : 青云客，4 腾讯智能闲聊，5:天行机器人，6 海知智能)
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

-  将 **is_alarm** 设置成 **True**。（当为 False 时，则关闭定时）  

```
alarm_info:
  is_alarm: True
```


#### 2.填写需要发送的好友信息

填写好友信息，例如：
```
alarm_timed:
  - "9:00"
  - "12:30"
  - "22:00"
wechat_name:
  - '文件传输助手'
  - '诗风'
group_name:
  - 'EverydayWechat 交流群'
city_name: '桂林'
dictum_channel : 3
start_date: '2017-10-10'
start_date_msg: '爱你的第{}天'
calendar: True
horescope: "处女座"
sweet_words: '你脚下的蚂蚁'
```

相关参数说明：

| 名称 | 示例       | 必填 | 说明 |
| -------- | -------------- | ---------- |---------- |
| wechat_name | '老婆' | 选填 | 好友名：可填多人。好友微信昵称或者备注名（不能输入微信号）|
| alarm_timed | '9：30' | 必填 | 定时时间，可填多个 |
| group_name | '交流群' | 选填 | 群聊名称，可填多个。必须要把需要的群聊保存到通讯录。|
| city_name | '成都' | 可空 | 城市名：朋友所在城市，用于发送天气。 |
| dictum_channel | 2 | 可空 | 格言渠道（见下表）|
| start_date | '2017-10-10' | 可空 | 相识日期：计算到当天的天数 。 |
| start_date_msg | '爱你的第{}天' | 可空 | 相识日期文案 |
| sweet_words | '来自你俊美的老公' | 可空 | 甜密的后缀。（钢铁直男的直描）|
| horescope | '处女座' | 可空 | 星座名或好友生日。用于发送星座运势 |
| calendar | True | 可空 | 万年历信息 |

**wechat_name**，**group_name** 至少要有一个。  

格言渠道 ： 1 : ONE●一个，2 : 词霸（每日双语），3: 土味情话， 4 : 一言，5：笑话，6: 民国情书，7: 彩虹屁。    

> Tips：可以把 **wechat_name**  填入『**文件传输助手**』，这样，提醒会发送到自己微信里的 **文件传输助手** 中。在不打扰别人的情况下，方便快速查看效果。


-  **alarm_time** 设置成需要提醒的时间。之后如果微信没有断线，即每天这个的时间会定时发送提醒。  

> 如果需要快速体验，可将 **alarm_timed** 当前系统时间之后的几分钟。例如当前时间为 11:35，并设置 5 分钟后发送提醒，即：alarm_timed：11：40

当然，也可设置另一套不同的方案。具体参考代码。  

一例提醒：  

```
2019-06-29 星期六 农历五月廿七 
【宜】嫁娶,祭祀,沐浴,扫舍,修饰垣墙 
【忌】行丧,安葬 
桂林天气预报 
【今日天气】阵雨
【今日温度】低温 26.0℃,高温 33.0℃ 
【今日风速】南风<3级
【出行提示】阵雨来袭，出门记得带伞 
处女座今日运势 
【幸运颜色】2
【幸运数字】薄荷绿
【综合运势】今天的你有机会重逢旧同学、旧朋友，对方会为你带来一些小惊喜，可能是某个不错的商机，也可能是某个消息。工作/学习上，今天的你目标性很强，能把当初奋斗的初心捡回来，重新出发。感情方面，有伴者今天要提防烂桃花的挑拨离间，多给对方一些信任。
你知道五氧化二磷被氧化前是什么样子嘛，什么样子？五二磷。 
宝贝这是我们在一起的第628天 
你脚下的蚂蚁
```

## 安装
首先，把 Python3 安装好，并配置好环境，个人建议新手安装 anaconda，具体安装教程，可自行谷歌搜索~  

直接下载此项目或 clone 项目到本地。  

使用 pip 安装依赖:

```
pip3 install -r requirements.txt
# pip install -r requirements.txt
```

## 运行：

在本地 cmd 中跳转项目目录下，运行:  

```
python run.py
```

第一次运行会跳出二维码，扫码登录。如输出日志中打印成：『登录成功』，则表示运行成功。  
登录成功后一段时间内再运行，微信会保持登录状态，不需要再扫码。  
如果需要切换用户，则在 *_config.yaml* 文件中，修改 *is_forced_switch* 的属性为 True。  

-  docker 下运行
    - 构建 `docker build -t everyday_wechat:v1 .`
    - 运行 `docker run everyday_wechat:v1`

## 示例截图：

![日志](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613171703.png)

![自动回复](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613162524.png)

## 提 [issues](https://github.com/sfyc23/EverydayWechat/issues) & 加群提问的建议。

-  当你拋出一个技术问题时，最终是否能得到有用的回答，往往取决于你所提问和追问的方式。推荐阅读：[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md)。    
-  **检查是否是最新的代码，检查是否是 Python3.5+，检查依赖有没有安装完整**。  
-  先检查微信是否可登录 [微信网页版](https://wx.qq.com/)，如网页端不能用，此项目也不能用。  
-  请更新你的 [itchat](https://github.com/littlecodersh/ItChat) 至最新版本 **1.3.10** 。查看 itchat 版本 **print(itchat.__version__ ）**。    
-  与微信相关的问题可以先去 itchat [issues](https://github.com/littlecodersh/ItChat/issues)， 查看是否有相似问题。  
-  微信名只能是昵称或者备注名，不能输入微信号。  
-  对群聊操作时，必须要把需要的群聊保存到通讯录。  
-  如果有新的思路和建议也欢迎提交。  

## Credits 致谢

本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。  

-  [wechatBot](https://github.com/gengchen528/wechatBot) —— 微信每日说，每日自动发送微信消息（Node + Wechaty）。   
-  [NodeMail](https://github.com/Vincedream/NodeMail) —— 用 Node 写一个爬虫脚本每天定时给女朋友发一封暖心邮件。  
-  [wechat-assistant](https://github.com/gengchen528/wechat-assistant) —— koa+wechaty实现的微信个人秘书，把你闲置的微信号利用起来做个个人秘书。  
-  [WechatRobot](https://github.com/scorego/WechatRobot) ——个人微信号自动回复、陪聊、查天气（Java）  
-  <https://github.com/likaixiang/EverydayWechat>   
-  <https://github.com/0xHJK/music-dl>  

## LICENSE
[MIT License](https://github.com/sfyc23/EverydayWechat/blob/master/LICENSE)


## 微信交流群
因为人数已超 100 人，请加 wx: **sfyc1314** 为好友，备注：「github」，好友会自动通过。  
通过后回复：「加群」，会自动拉你入群。  
机器人二维码： 

![微信交流群](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190614125724.png)
