# coding=utf-8
"""
https://github.com/MZCretin/RollToolsApi#%E9%9A%8F%E6%9C%BA%E8%8E%B7%E5%8F%96%E7%AC%91%E8%AF%9D%E6%AE%B5%E5%AD%90%E5%88%97%E8%A1%A8
随机获取笑话段子列表
"""
import requests

def get_rtjokes_info():
    """
    随机获取笑话段子列表(https://github.com/MZCretin/RollToolsApi#%E9%9A%8F%E6%9C%BA%E8%8E%B7%E5%8F%96%E7%AC%91%E8%AF%9D%E6%AE%B5%E5%AD%90%E5%88%97%E8%A1%A8)
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
