# coding=utf-8
"""
https://www.sojson.com/api/lunar.html
指定日期的节假日及万年历信息
"""
from datetime import datetime
import requests
from everyday_wechat.utils.common import (
    WEEK_DICT,
    SPIDER_HEADERS
)


def get_sojson_calendar(date=''):
    """
    获取指定日期的节假日及万年历信息
     https://www.sojson.com/api/lunar.html
    :param data: str 日期 格式 %Y-%m-%d
    :rtype str
    """
    date_ = date or datetime.now().strftime('%Y-%m-%d')
    # print('获取 {} 的日历...'.format(date_))
    try:
        resp = requests.get('https://www.sojson.com/open/api/lunar/json.shtml?date={}'.format(date_),
                            headers=SPIDER_HEADERS)
        if resp.status_code == 200:
            """
            {"code":1,"msg":"数据返回成功","data":{
            "date":"2019-06-27","weekDay":4,"yearTips":"己亥",
            "type":0,"typeDes":"工作日","chineseZodiac":"猪","solarTerms":"夏至后",
            "avoid":"移徙.入宅.安葬","lunarCalendar":"五月廿五",
            "suit":"订盟.纳采.出行.祈福.斋醮.安床.会亲友",
            "dayOfYear":178,"weekOfYear":26,"constellation":"巨蟹座"}}
            """
            # print(resp.text)
            content_dict = resp.json()
            if content_dict['status'] == 200:
                data_dict = content_dict['data']
                # 农历
                lunar_calendar = '{}月{}'.format(data_dict['cnmonth'], data_dict['cnday'])
                # 二十四节气
                # solarTerms = data_dict['jieqi'].get(str(data_dict['day']), '')
                # print(data_dict['jieqi'])
                suit = data_dict['suit']
                suit = suit if suit else '无'
                taboo = data_dict['taboo']
                taboo = taboo if taboo else '无'
                return_text = '{date} {week} 农历{lunarCalendar}\n【宜】{suit}\n【忌】{taboo}'.format(
                    date=date,
                    week=WEEK_DICT[data_dict['week']],
                    lunarCalendar=lunar_calendar,
                    suit=suit,
                    taboo=taboo,
                )
                return return_text
            else:
                print('获取日历失败:{}'.format(content_dict['message']))

        print('获取日历失败。')
    except Exception as exception:
        print(str(exception))
    return None


get_calendar = get_sojson_calendar

if __name__ == '__main__':
    # date = datetime.now().strftime('%Y-%m-%d')
    # date = '2018-11-06'
    # content = get_calendar(date)
    # print(content)
    pass
