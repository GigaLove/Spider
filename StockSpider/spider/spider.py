# -*- coding: utf-8 -*-
import random
import urllib2
import json
from datetime import datetime
from datetime import timedelta
import time


class StockSpider:
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]

    url = 'http://batstrading.com/json/%s/book/%s'
    headers = {'Referer': 'http://batstrading.com'}
    stock_types = ['bzx', 'byx', 'edgx', 'edga']
    # stock_names = ['SPY', 'JCP', 'BAC', 'GDX', 'DUST', 'NVDA', 'VXX', 'AAPL', 'EEM', 'MT']
    stock_names = ['SPY', 'JCP', 'BAC', 'GDX']
    data_path = '../stock-data/stock-%s-%s.txt'

    def __init__(self):
        pass

    def spider(self):
        while True:
            if self.is_trade_time():
                cur_date = self.get_usa_date()
                for stock_name in self.stock_names:
                    for stock_type in self.stock_types:
                        stock_url = self.url % (stock_type, stock_name)
                        try:
                            self.headers['User-agent'] = self.random_user_agent()
                            request = urllib2.Request(stock_url, None, self.headers)
                            response = urllib2.urlopen(request)
                            stock_json = json.loads(response.read(), 'utf-8')
                            if stock_json is not None and 'success' \
                                    in stock_json and stock_json['success']:
                                self.parse(stock_name, stock_type, cur_date, stock_json['data'])
                        except urllib2.URLError, e:
                            if hasattr(e, "code"):
                                print e.code
                            if hasattr(e, "reason"):
                                print e.reason
                        except StandardError, e:
                            print e.message
                    time.sleep(1)

    def random_user_agent(self):
        return self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS) - 1)]

    def parse(self, stock_name, stock_type, date, stock_info):
        stock_info['timestamp'] = date + ' ' + stock_info['timestamp']
        with open(self.data_path % (stock_name, stock_type), 'a') as f:
            content = json.dumps(stock_info, encoding='utf-8')
            # print content
            f.write(content + '\n')

    @staticmethod
    def is_trade_time():
        now = datetime.now()
        zone_delta = timedelta(hours=12)
        usa_now = now - zone_delta
        weekday = usa_now.weekday()
        if weekday == 5 or weekday == 6:
            return False
        else:
            begin = usa_now.replace(hour=9, minute=30, second=0)
            end = usa_now.replace(hour=16, minute=0, second=0)
            if begin <= usa_now <= end:
                return True
            return False

    @staticmethod
    def get_usa_date():
        now = datetime.now()
        zone_delta = timedelta(hours=12)
        usa_now = now - zone_delta
        return usa_now.strftime("%Y-%m-%d")


if __name__ == '__main__':
    stock_spider = StockSpider()
    stock_spider.spider()
