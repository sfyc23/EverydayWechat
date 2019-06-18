# coding=utf-8
"""
句子迷：（https://www.juzimi.com/）
民国情书：朱生豪先生的情话 && 爱你就像爱生命
Author: ClaireYiu(https://github.com/ClaireYiu)
"""
import random
from requests_html import HTMLSession

def get_zsh_info():
    """
    句子迷：（https://www.juzimi.com/）
    :return: str 情话
    """
    print('正在获取民国情话...')
    try:
        name = [['writer/朱生豪', 38, 'xqfamoustermspage'], ['article/爱你就像爱生命', 22, 'xqarticletermspage']]
        apdix = random.choice(name)
        url = 'https://www.juzimi.com/{}?page={}'.format(apdix[0], random.randint(0, apdix[1] - 1))
        # print(url)
        resp = HTMLSession().get(url)
        if resp.status_code == 200:
            num = random.randint(1, 10)
            mode = 'even' if num % 2 == 0 else 'odd'
            block = apdix[2]
            sel = '#block-views-' + block + '-block_1 > div > div > div > div > div.view-content > div.views-row.views-row-' + str(
                num) + '.views-row-' + mode + ' > div > div.views-field-phpcode-1 > a'
            results = resp.html.find(sel)
            return results[0].text
        print('获取民国情话失败..')
        return None
    except Exception as exception:
        print(exception)
        return None
    return None

get_one_words = get_zsh_info

if __name__ == '__main__':
    for _ in range(100):
        # ow = get_one_words()
        # print(ow)
        print(random.randint(1, 10))
