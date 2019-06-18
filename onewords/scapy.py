from requests_html import HTMLSession
import random


def get_zsh_info():
    session = HTMLSession()
    name = [['writer/朱生豪', 38], ['article/爱你就像爱生命', 22]]
    picNum = random.randint(0, 1)
    apdix = name[picNum]
    url = 'https://www.juzimi.com/' + apdix[0]
    # print(url)
    urls = []

    urls.append(url)
    for i in range(1, apdix[1]):
        urls.append(url + '?page=' + str(i))
    # print(urls)

    slct = urls[random.randint(0, apdix[1] - 1)]
    #print(slct)
    r = session.get(slct)
    #print(slct)

    num = random.randint(1, 10)
    mode = 'even' if num % 2 == 0 else 'odd'
    block = 'xqarticletermspage' if picNum == 1 else 'xqfamoustermspage'
    sel = '#block-views-'+block+'-block_1 > div > div > div > div > div.view-content > div.views-row.views-row-' + str(
        num) + '.views-row-' + mode + ' > div > div.views-field-phpcode-1 > a'

    results = r.html.find(sel)
    #print(results)
    #print(results[0].text)
    return results[0].text


get_one_words = get_zsh_info
