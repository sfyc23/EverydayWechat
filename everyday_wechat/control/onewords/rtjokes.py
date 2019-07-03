# coding=utf-8
"""
https://github.com/MZCretin/RollToolsApi#随机获取笑话段子列表
随机获取笑话段子列表
"""
import requests

def get_rtjokes_info():
    """
    随机获取笑话段子列表(https://github.com/MZCretin/RollToolsApi#随机获取笑话段子列表)
    :return: str,笑话。
    """
    print('获取随机笑话...')
    try:
        resp = requests.get('https://www.mxnzp.com/api/jokes/list/random')
        # print(resp.text)
        if resp.status_code == 200:
            content_dict = resp.json()
            if content_dict['code'] == 1:
                # 每次返回 10 条笑话信息，只取一次
                return_text = content_dict['data'][0]['content']
                # print(return_text)
                return return_text
            else:
                print(content_dict['msg'])
        print('获取笑话失败。')
    except Exception as exception:
        print(exception)
        return None
    return None


get_one_words = get_rtjokes_info

if __name__ == '__main__':
    get_rtjokes_info()
