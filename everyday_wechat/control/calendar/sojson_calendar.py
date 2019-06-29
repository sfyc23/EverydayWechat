# coding=utf-8
"""
https://www.sojson.com/api/lunar.html
指定日期的节假日及万年历信息
"""
import requests
from datetime import datetime
from everyday_wechat.utils.common import (
    WEEK_DICT,
    SPIDER_HEADERS
)


def get_sojson_calendar(date=''):
    """
    获取指定日期的节假日及万年历信息
     https://github.com/MZCretin/RollToolsApi#指定日期的节假日及万年历信息
    :param data: str 日期 格式 yyyyMMdd
    :rtype str
    """
    date = date or datetime.now().strftime('%Y-%m-%d')
    # print('获取 {} 的日历...'.format(date))
    try:
        resp = requests.get('https://www.sojson.com/open/api/lunar/json.shtml?date={}'.format(date),
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
            if resp.json()['status'] == 200:
                data_dict = resp.json()['data']
                # 农历
                lunarCalendar = '{}月{}'.format(data_dict['cnmonth'], data_dict['cnday'])
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
                    lunarCalendar=lunarCalendar,
                    suit=suit,
                    taboo=taboo,
                )
                return return_text
            else:
                print('获取日历失败:{}'.format(resp.json()['message']))

        print('获取日历失败。')
    except Exception as exception:
        print(exception)


get_calendar = get_sojson_calendar

if __name__ == '__main__':
    # date = datetime.now().strftime('%Y-%m-%d')
    date = '2018-11-06'
    content = get_calendar(date)
    print(content)
    # print('https://www.sojson.com/open/api/lunar/json.shtml?date={}'.format(date))
