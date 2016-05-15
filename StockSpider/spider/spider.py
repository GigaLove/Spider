# -*- coding: utf-8 -*-

import urllib2
import json
from datetime import datetime
from datetime import timedelta
import time


class StockSpider:
    url = 'http://batstrading.com/json/%s/book/%s'
    headers = {'User-Agent': '"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"',
               'Referer': 'http://batstrading.com'}
    stock_types = ['bzx', 'byx', 'edgx', 'edga']
    stock_names = ['SPY', 'JCP', 'BAC', 'GDX', 'DUST', 'NVDA', 'VXX', 'AAPL', 'EEM', 'MT']
    data_path = '../data/stock-%s-%s-%s.csv'

    def __init__(self):
        pass

    def spider(self):
        while True:
            cur_date = self.get_usa_date()
            if self.is_trade_time():
                for stock_type in self.stock_types:
                    for stock_name in self.stock_names:
                        stock_url = self.url % (stock_type, stock_name)
                        request = urllib2.Request(stock_url, None, self.headers)
                        response = urllib2.urlopen(request)
                        stock_json = json.loads(response.read(), 'utf-8')
                        if stock_json['success']:
                            self.parse(stock_name, stock_type, stock_json['data'], cur_date)
                        time.sleep(2)

    def parse(self, stock_name, stock_type, stock_info, date):
        # timestamp = date + stock_info['timestamp']
        # asks = stock_info['asks']
        # bids = stock_info['bids']
        # trades = stock_info['trades']
        with open(self.data_path % (stock_name, stock_type, date), 'a') as f:
            content = json.dumps(stock_info, encoding='utf-8')
            print content
            f.write(content + '\n')

    @staticmethod
    def is_trade_time():
        now = datetime.now()
        zone_delta = timedelta(hours=12)
        usa_now = now - zone_delta
        begin = usa_now.replace(hour=9, minute=30, second=0)
        end = usa_now.replace(hour=16, minute=30, second=0)
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
