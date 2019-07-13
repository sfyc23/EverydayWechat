# coding=utf-8
"""
句子迷：（https://www.juzimi.com/）
民国情书：朱生豪先生的情话 && 爱你就像爱生命
Author: ClaireYiu(https://github.com/ClaireYiu)
"""
import random
import requests
# from requests_html import HTMLSession


def get_zsh_info():
    """
    句子迷：（https://www.juzimi.com/）
    朱生豪：https://www.juzimi.com/writer/朱生豪
    爱你就像爱生命（王小波）：https://www.juzimi.com/article/爱你就像爱生命
    三行情书：https://www.juzimi.com/article/25637
    :return: str 情话
    """
    print('正在获取民国情话...')
    try:
        name = [
            ['writer/朱生豪', 38,],
            ['article/爱你就像爱生命', 22],
            ['article/25637', 55],
                ]
        apdix = random.choice(name)
        # page 从零开始计数的。
        url = 'https://www.juzimi.com/{}?page={}'.format(
            apdix[0], random.randint(1, apdix[1]))
        # print(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            # print(resp.html)
            # results = resp.find('a.xlistju')
            # if results:
            #     re_text = random.choice(results).text
            #     if re_text and '\n\n' in re_text:
            #         re_text = re_text.replace('\n\n','\n')
            #     return re_text
            return None
        print('获取民国情话失败..')
    except Exception as exception:
        print(exception)
    return None


get_one_words = get_zsh_info

if __name__ == '__main__':
    # for _ in range(15):
    #     ow = get_one_words()
    #     print(ow)
    pass
