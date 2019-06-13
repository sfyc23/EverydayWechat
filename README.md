![python_vesion](https://img.shields.io/badge/Python%20-%3E%3D%203.5-green.svg)  

[EverydayWechat](https://github.com/sfyc23/EverydayWechat) 是基于 Python3 与 [Itchat](https://github.com/littlecodersh/ItChat) 的微信小工具。  
可以定时给朋友发送每日天气、提醒、每日一句，也可以智能自动回复好友信息。  
操作简单，小白用户也可快速上手。


## 功能说明

- 支持对多个微信好友自动回复。
- 定时发送提醒，内容包括（天气、格言、自定义的话）。

> 注意：仅支持 Python3，建议使用 **Python3.5 以上版本**

## 相关数据来源

### 天气信息：

- SOJSON：<https://www.sojson.com/blog/305.html>

### 每日一句：

- ONE ● 一个： <http://wufazhuce.com/>
- 金山词霸 ● 每日一句（双语）：<http://open.iciba.com/?c=api>
- 一言 ：<https://hitokoto.cn/>
- 土味情话： <https://www.v2ex.com/t/569853> (目前已失联)

### 人工智能机器人

- 图灵机器人：<http://www.turingapi.com/>（需求实名制认证，并每天免费数量只有100条）
- 青云客智能聊天机器人：<http://api.qingyunke.com/>（直接能用，无数量限制，但有点智障，分手神器。图灵机器人的备胎）

计划再想加上幽默段子，养生之类的数据来源，欢迎提供相关网页与接口。

## 项目配置
目前项目所有的配置都是在 **[_config.yaml](https://github.com/sfyc23/EverydayWechat/blob/master/_config.yaml)** 文件中。  
配置文件请严格遵循 yaml 语法格式，yaml 学习地址:  
<https://ansible-tran.readthedocs.io/en/latest/docs/YAMLSyntax.html>    
<http://einverne.github.io/post/2015/08/yaml.html>

### 配置自动回复机器人。

#### 1. 开启自动回复
将 **is_auto_relay** 设置为：True。

#### 2. 配置图灵机器人
打开图灵机器人官网：[http://www.turingapi.com](http://www.turingapi.com/) 进行注册。  
创建机器人，得到 apikey，userid。  
将填入到 **_config.yaml** 文件中的：
```
turing_conf:
  apiKey: '你所获取apikey'
  userId: '你所获取的userId'
```
> 图灵机器人必须认证后才能使用，免费版用户，每天可使用 100 条信息，且用且珍惜。

#### 3. 指定自动回复的好友名单

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
6. 当没有图灵机器人 apikey 与 UserId，或者数量超出时，会使用备用的青云客智能聊天机器人获取数据。

### 配置定时提醒
#### 1.开启并设置提醒时间

* 将 **is_alarm** 设置成 **True**。（当为 False 时，则关闭定时）
* **alarm_time** 设置成需要提醒的时间。之后如果微信没有断线，即每天这个的时间会定时发送提醒。

如果需要快速体验，可将 **alarm_timed** 当前系统时间之后的几分钟。例如当前时间为 11:35，并设置 5 分钟后发送提醒。
```
alarm_info:
  is_alarm: True
  #定时发送时间
  alarm_timed: '11:40'
```

#### 2.填写需要发送的好友信息

填写好友信息，例如：
```
girlfriend_infos:
  #  如果你有多个好友需要发送，则参照这个样式，复制即可
  - wechat_name: '宝宝'
    city_name: '朝阳区'
    dictum_channel : 4
    start_date: '2011-11-11'
    sweet_words: '来自最爱你的我。'
```

相关参数说明：

| 名称 | 示例       | 必填 | 说明 |
| -------- | -------------- | ---------- |---------- |
| wechat_name | '老婆' | 必填 |好友名：需要发送的人的微信昵称或者备注名（不能输入微信号）|
| city_name | '成都' | 可空| 城市名：女友所在城市，用于发送天气。 |
| dictum_channel | 2 |可空|格言渠道（1 : ONE●一个，2 : 词霸（双语）， 4 : 一言)|
| start_date | '2017-10-10' | 可空 |相识日期：计算到当前天的天数 。|
| sweet_words |'来自你俊美的老公' | 可空 |甜密的后缀。（钢铁直男的直描）|


如果全填，最终显示效果：

>  Without you, today's emotions would be the scurf of
> yesterday's.如果没有你，如此的良辰美景让我去向何人诉说？  
2019-06-13 星期四 多云 北风 <3级 高温 29.0℃ 低温 22.0℃ 阴晴之间，谨防紫外线侵扰  
宝贝这是我们在一起的第 611 天。  
来自最爱你的我。

本项目在以下环境以测试通过：

| 系统名称 | 系统版本       | Python版本 |
| -------- | -------------- | ---------- |
| Windows  | Windows 10 x 64 | 3.6.5      |


## 安装

下载或 clone 项目到本地。  

### 安装依赖:

```
pip3 install -r requirements.txt
```

## 运行：


在本地 cmd 中跳转项目目录下，运行：
```
python run.py
```

第一次运行会跳出二维码，扫码登录。如输出日志中打印成：『登录成功』，则表示运行成功。 
之后一段时间再运行，微信会保持登录状态，不需要再扫码。  
如果需要切换用户，则在 *_config.yaml* 文件中，修改 *is_forced_switch* 的属性为 True。

## 示例截图：

![日志](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613171703.png)

![自动回复](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613162524.png)

## 提 [issues](https://github.com/sfyc23/EverydayWechat/issues) 说明

- **检查是否是最新的代码，检查是否是 Python3.5+，检查依赖有没有安装完整**。
- 先检查微信是否可登录 [微信网页版](https://wx.qq.com/)，如网页端不能用，此项目也不能用。
- 请更新你的 [itchat](https://github.com/littlecodersh/ItChat) 为最新版本。
- 与微信相关的问题可以先去 itchat [issues](https://github.com/littlecodersh/ItChat/issues)， 查看是否有相似问题。
- 微信名只能是昵称或者备注名，不能输入微信号。
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

![交流群](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613174556.png)  
 
## 联系我

微博：[诗风悠存](https://weibo.com/sfyc23)