# -*- coding: utf-8 -*-
# 于丽美
# http://journals.sagepub.com/toc/bnaa/2
import scrapy
from qikan.items import QikanItem
import re
import time
import sys,os
from qikan.config import Config,proxyRequest

class MySpider(scrapy.Spider):
    name = '56wen'
    start_urls = ['http://www.56wen.com']
    base_url = 'http://www.56wen.com'
    def parse(self, response):
        print('-------首页header所有分类-------')
        hrefs = response.xpath("//ul[@class='cl']/li/a/@href").extract()
        print('一共 %s 个分类' % len(hrefs))
        print(hrefs)
        print('---------------------')
        for i in range(len(hrefs)):
            url = hrefs[i]
            print('Go to:',url)
            yield proxyRequest(url=url, callback=self.parseBookList)

    def parseBookList(self, response):
        hrefs = response.xpath("//div[@class='list_l_box']//h4/a/@href").extract()
        print('-------book列表页-------')
        print('本页一共 %s 本书' % len(hrefs))
        hrefs=list(map(lambda x:self.base_url + x,hrefs))
        print(hrefs)
        print('---------------------')        

        for i in range(len(hrefs)):
            url = hrefs[i]
            print('Go to:',url)
            yield proxyRequest(url=url, callback=self.parseBookIntro)
        
        # print('--------下一页---------')
        # nextHref = response.xpath("//li[@class='next']/a/@href").extract()
        # nextHref = self.base_url + nextHref[0]
        # print('Go to next page:',nextHref)
        # yield proxyRequest(url=nextHref, callback=self.parseBookList)

    def parseBookIntro(self, response):
        print('-------book介绍页，进入“查看全部章节”-------')
        hrefs = response.xpath("//div[@class='ft']/a/@href").extract()
        href = hrefs[0]
        if 'http' not in href:
            print('href补全，自动补全base_url')
            href = self.base_url + href
        print(href)
        print('---------------------')

        yield proxyRequest(url=href, callback=self.parseBookIndex)
    
    def parseBookIndex(self,response):
        title=response.xpath("//div[@class='catalog_hd']/h1/text()").extract()[0]
        # title=response.xpath("//div[@class='cont']/h1/text()").extract()[0]
        print('title',title)
        filePath = os.path.join(Config().corpusPath,title+'.txt')
        if os.path.exists(filePath) == True:
            print(filePath)
            print('------文章已爬过，跳过------------')
            print('------文章已爬过，跳过------------')
            return False

        print('-------章节目录页-------')
        hrefs = response.xpath("//ul[@class='catalog_list clearfix']/li/a/@href").extract()
        print('一共 %s 个章节' % len(hrefs))
        hrefs=list(map(lambda x:self.base_url + x,hrefs))
        print(hrefs)
        for i in range(len(hrefs)):
            print('Go to 内容页:',hrefs[i])
            # time.sleep(1)
            yield proxyRequest(url=hrefs[i], callback=self.parseContentWrapper(title))
    
    def parseContentWrapper(self,title):
        def parseContent(response):
            content = response.xpath("//div[@id='J_article_con']/text()").extract()
            print('-------爬取内容：-------')
            print(title)
            print(content[0:20])
            yield {'title':title,'content':content}
        return parseContent



        









