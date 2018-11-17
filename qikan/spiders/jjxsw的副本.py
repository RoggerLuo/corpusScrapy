# -*- coding: utf-8 -*-
# 于丽美
# http://journals.sagepub.com/toc/bnaa/2
import scrapy
from qikan.items import QikanItem
import re
import time
import sys

from qikan.config import Config,postItemWithPdf,proxyRequest

class SageSpider(scrapy.Spider):
    name = 'Test'
    start_urls = ['https://www.csdn.net/']
    base_url = 'https://www.csdn.net'

    def parse(self, response):
        hrefs = response.xpath("//div[@class='nav_com']/ul/li/a/@href").extract()
        print('-------首页类别-------')
        print(len(hrefs))
        print('------------------------')
        hrefs = hrefs[3:]
        for i in range(3): #len(hrefs)
            url = self.base_url+hrefs[i]
            print('Go to:',url)
            yield proxyRequest(url=url, callback=self.parse2)

    def parse2(self, response):
        print('-------parse2爬取结果-------')
        hrefs = response.xpath("//main//ul/li/div[@class='list_con']/div[@class='title']/h2/a/@href").extract()
        print(hrefs)
        print('---------------------')
        for i in range(2): #len(hrefs)
            print('Go to(X2):',hrefs[i])
            yield proxyRequest(url=hrefs[i], callback=self.parse3)
    
    def parse3(self, response):
        print('-------parse3爬取结果-------')
        hrefs = response.xpath("//article//p/text()").extract()
        print(hrefs)
        print('---------------------')




        









