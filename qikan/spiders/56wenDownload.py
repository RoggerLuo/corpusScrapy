# -*- coding: utf-8 -*-
# 于丽美
# http://journals.sagepub.com/toc/bnaa/2
import scrapy
from qikan.items import QikanItem
import re
import time
import sys,os
from qikan.config import Config,proxyRequest,postItemWithPdf

class MySpider(scrapy.Spider):
    name = '56wenDownload'
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
        
        print('--------下一页---------')
        nextHref = response.xpath("//li[@class='next']/a/@href").extract()
        if len(nextHref) == 0:
            print('------没有下一页了---------')            
            return
        nextHref = self.base_url + nextHref[0]
        print('Go to next page:',nextHref)
        yield proxyRequest(url=nextHref, callback=self.parseBookList)

    def parseBookIntro(self, response):
        print('-------book介绍页，进入“下载阅读”-------')
        hrefs = response.xpath("//a[@class='albumdown dnum1']/@href").extract()
        href = hrefs[0]
        #print(href)
        if 'http' not in href:
            print('href补全，自动补全base_url')
            href = self.base_url + href
        print(href)
        print('---------------------')
        yield proxyRequest(url=href, callback=self.parseBookDownload)
    
    def parseBookDownload(self,response):
        print('-------parseBookDownload-------')
        href=response.xpath("//div[@class='xzxx']//p/a/@href").extract()[0] 
        title=response.xpath("//div[@class='xzxx']//p/a/font/b/text()").extract()[0] 
        title=title[:-6]
        print('download href:',href)
        print('开始下载 开始下载',title)
        yield proxyRequest(url=href, meta={'filename': title + '.txt'},callback=postItemWithPdf({}))

        # yield {'download':True,'href':href}