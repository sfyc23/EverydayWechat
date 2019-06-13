# coding=utf-8

"""
http://api.qingyunke.com/
青云客智能聊天机器人API
可直接使用
"""
import requests

URL = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'

def get_qingyunke(text):
    try:
        # print('发出消息:{}'.format(text))
        resp = requests.get(URL.format(text))
        if resp.status_code == 200:
            # print(resp.text)
            re_data = resp.json()
            if re_data['result'] == 0:
                return_text = re_data['content']
                return return_text
        print('获取数据失败')
        return None
    except Exception as e:
        print(e)
        return None
    return None


get_auto_reply = get_qingyunke

if __name__ == '__main__':
    text = '少年阿宾'
    rt = get_qingyunke(text)
    print('回复：', rt)
