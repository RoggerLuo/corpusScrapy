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
    name = '56wen'
    start_urls = ['http://www.56wen.com']
    base_url = 'http://www.56wen.com'
    def parse(self, response):
        hrefs = response.xpath("//ul[@class='cl']/li/a/@href").extract()
        print('-------首页header所有分类-------')
        print(len(hrefs))
        # hrefs=list(map(lambda x:self.base_url + x,hrefs))
        print(hrefs)
        print('---------------------')        
        for i in range(3): #len(hrefs)
            url = hrefs[i]
            print('Go to:',url)
            yield proxyRequest(url=url, callback=self.parse2)
    def parse2(self, response):
        hrefs = response.xpath("//div[@class='list_l_box']//h4/a/@href").extract()
        print('-------小说列表分页-------')
        print(len(hrefs))
        hrefs=list(map(lambda x:self.base_url + x,hrefs))
        print(hrefs)
        print('---------------------')        
        print(hrefs)
        yield proxyRequest(url=url, callback=self.parseNextCatePage)

        return
        for i in range(3): #len(hrefs)
            url = hrefs[i]
            print('Go to:',url)
            yield proxyRequest(url=url, callback=self.parse2)

    def parse22(self, response):
        print('-------章节目录页，进入“查看全部章节”-------')
        hrefs = response.xpath("//div[@class='ft']/a/@href").extract()
        print(hrefs)
        print('---------------------')
        return
        # hrefs = response.xpath("//main//ul/li/div[@class='list_con']/div[@class='title']/h2/a/@href").extract()

        for i in range(2): #len(hrefs)
            print('Go to(X2):',hrefs[i])
            yield proxyRequest(url=hrefs[i], callback=self.parse3)
    
    def parseNextCatePage(self, response):
        next
        print('-------parse3爬取结果-------')
        hrefs = response.xpath("//article//p/text()").extract()
        print(hrefs)
        print('---------------------')




        









