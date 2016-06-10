# -*- coding: utf-8 -*-

import urllib2
import re

from lxml import etree


class DoubanSpider:

    def __init__(self):
        self.url = 'https://movie.douban.com/top250'

    def get_content(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) "
                                 "Gecko/20100101 Firefox/46.0"}
        req = urllib2.Request(self.url, headers=headers)
        try:
            resp = urllib2.urlopen(req)
            content = resp.read()
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print e.reason
        else:
            # self.re_parse(content)
            self.xpath_parse(content)

    @staticmethod
    def re_parse(content):
        pattern = re.compile(r'<span class="title">(.*?)</span>', re.S)
        res = re.search(pattern, content)
        if res:
            print res.group(1)

    @staticmethod
    def xpath_parse(content):
        html = etree.HTML(content)
        titles = html.xpath('//ol[@class="grid_view"]/li/div[@class="item"]/'
                            'div[@class="info"]/div[@class="hd"]/a/span[1]/text()')
        for title in titles:
            print title

if __name__ == '__main__':
    douban = DoubanSpider()
    douban.get_content()
