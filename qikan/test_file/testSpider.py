# -*- coding: utf-8 -*-
# 于丽美
# http://journals.sagepub.com/toc/bnaa/2
import scrapy
from qikan.items import QikanItem
import re
import time
from .config import Config,postItemWithPdf,postItem,proxyRequest

class SageSpider(scrapy.Spider):
    name = 'Test'
    # url = input('请输入网址：')
    start_urls = ['http://ip.filefab.com/index.php']
    base_url = 'http://ip.filefab.com/index.php'

    def parse(self, response):
        # 文章url
        # hrefs = response.xpath("//div[@class='art_title linkable']/a[@class='ref nowrap']/@href").extract()
        # volume = response.xpath("//div[@class='pager issueBookNavPager']/span[@class='journalNavCenterTd']/div[@class='journalNavTitle']/text()").extract()[0]
        print('-------原始爬取结果-------')

        print(response.xpath("//h1[@id='ipd']/span/text()").extract()[0])

        for i in range(10):
            print(time.time())
            yield proxyRequest(url=self.base_url+'?v='+str(i),meta={}, callback=self.parse2)

    def parse2(self, response):
        print('-------爬取结果-------')
        
        print(response.xpath("//h1[@id='ipd']/span/text()").extract()[0])
        print('---------------------')
