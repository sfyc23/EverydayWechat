![python_vesion](https://img.shields.io/badge/Python%20-%3E%3D%203.5-green.svg)  

[EverydayWechat](https://github.com/sfyc23/EverydayWechat) 是基于 Python3 与 Itchat 的微信小工具。  
可以定时给朋友发送每日天气、提醒、每日一句，也可以智能自动回复好友信息。




## 功能说明

- 支持对多个微信好友自动回复。
- 定时发送提醒，内容包括（天气、格言、自定义的话）。

> 注意：仅支持 Python3，建议使用 **Python3.5 以上版本**

## 相关数据来源

- 天气信息来自：[SOJSON](https://www.sojson.com/blog/305.html) 
- 每日一句和上面的大佬一样也是来自 [ONE●一个](http://wufazhuce.com/)
- 金山词霸 ● 每日一句（英文加中文）：[iciba](http://open.iciba.com/?c=api)
- 一言 ：[hitokoto](https://hitokoto.cn/)
- 土味情话： [渣男在线](https://www.v2ex.com/t/569853)(目前失联中)
- 图灵机器人：<http://www.turingapi.com/>（需求实名制认证，并每天免费数量只有100条）
- 青云客智能聊天机器人：<http://api.qingyunke.com/>（直接能用，无限制数量，但回复不太智能。图灵机器人的备胎）

## 项目配置
所有项目相关都是 **[_config.yaml](https://github.com/sfyc23/EverydayWechat/blob/master/_config.yaml)** 文件中。
配置文件请严格遵循 yaml 语法格式，yaml 学习地址:
https://ansible-tran.readthedocs.io/en/latest/docs/YAMLSyntax.html
http://einverne.github.io/post/2015/08/yaml.html

### 配置自动回复机器人。

#### 1. 开启自动回复：
将 **is_auto_relay** 设置为：True。
#### 2. 配置图灵机器人:
打开图灵机器人官网：[http://www.turingapi.com](http://www.turingapi.com/) 进行注册。  
创建机器人，得到 apikey，userid。  
将填入到 **_config.yaml** 文件中的：
```
turing_conf:
  apiKey: '你所获取'
  userId: '你所获取的userId'
```
> 图灵机器人必须认证后才能使用，免费版用户，每天可使用 100 条信息，且用且珍惜。

#### 3. 指定自动回复的好友名单:
```
# 指定自动回复的好友名单。
auto_reply_names:
  - '好友1'
  - '好友2'
```

关于自动回复，目前可以公开的情报：
1. 只能自动回复文字类消息；
3. 群消息自动回复还未现实。（待完成）；
4. 如果消息发送太频繁，微信会限制登录网页端登录。放心，并不会封号；
5. 并不是对所有人自动回复，只是回复 girlfriend_infos 中的人。
6. 当没有图灵机器人 apikey 与 UserId，或者数量失效时。会使用备用的青云客智能聊天机器人获取数据。

### 配置定时提醒
#### 1.开启并设置提醒时间
如：
```
alarm_info:
  is_alarm: True
  #定时发送时间
  alarm_timed: '9:30'
```
关闭将 is_alarm 设置为：False

#### 2.填写需要发送的好友。
如：
```
girlfriend_infos:
  - #女友微信昵称或者备注名，不能输入微信号。
    wechat_name: '古典'
    #女友所在城市，用于发送天气。（可空）
    city_name: '桂林'
    # 从那天开始勾搭的（可空）(最终效果为：宝贝这是我们在一起的第 111 天)
    start_date: '2017-10-10'
    # 后缀（可空）
    sweet_words: '来自最爱你的我。'

  #如果你有多个人需要发送，则参照这个样式，复制即可
  #如不需要，则删除或注解下面所有的数据
  - wechat_name: 'happy'
    city_name: '朝阳区'
    start_date: '2018-11-11'
    sweet_words: '来自你俊美的老公。'
```



本项目在以下环境以测试通过：

| 系统名称 | 系统版本       | Python版本 |
| -------- | -------------- | ---------- |
| Windows  | Windows 10 x 64 | 3.6.5      |


## 安装

下载或 clone 项目到本地。  

### 安装依赖:
在本地 cmd 中跳转项目目录下，运行：
```
pip3 install -r requirements.txt
```

### 直接运行:
```
python run.py
```

## 示例截图：

日志：
![日志](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613171703.png)

自动回复：
![自动回复](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613162524.png)

## 提 [issues](https://github.com/sfyc23/EverydayWechat/issues) 说明

- **检查是否是最新的代码，检查是否是 Python3.5+，检查依赖有没有安装完整**。
- 先检查微信是否可登录 [微信网页版](https://wx.qq.com/)，如网页端不能用，此项目也不能用。
- 请更新你的 [itchat](https://github.com/littlecodersh/ItChat) 为最新版本。
- 与微信相关的可以先去 itchat [issues](https://github.com/littlecodersh/ItChat/issues) 是否有相似问题。
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

![交流群](https://raw.githubusercontent.com/sfyc23/image/master/vlog/20190613173641.jpg)