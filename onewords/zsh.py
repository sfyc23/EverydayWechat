from requests_html import HTMLSession
import random

def get_zsh_info():
    session = HTMLSession()
    url = 'https://www.juzimi.com/writer/朱生豪'

    urls = []

    urls.append(url)
    for i in range(1, 38):
        urls.append(url + '?page=' + str(i))


    slct = urls[random.randint(0,36)]

    r = session.get(slct)

    num = random.randint(1,10)
    mode = 'even' if num % 2 ==0 else 'odd'
    sel = '#block-views-xqfamoustermspage-block_1 > div > div > div > div > div.view-content > div.views-row.views-row-'+str(num)+'.views-row-'+mode+' > div > div.views-field-phpcode-1 > a'

    results = r.html.find(sel)

    return results[0].text

get_one_words = get_zsh_info()

#print(get_one_words)
