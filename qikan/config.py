from urllib import request, parse
import json
import requests
import os
import sys
import scrapy
import time
import os
import random

apiAddress = 'http://47.99.79.11:8081'
proxyServer = "http://transfer.mogumiao.com:9001"
proxyAuth = "Basic " + 'Y0tZdUFEc0tEQjNTOHVtNDp0dTQwaUNJUFQ0cWRKMnow'

class Config(object):
    pdf_url = os.getcwd() + '/'  #'/Users/RogersMac/WorkHtgk/pythonScrapy/qikan1demon/qikan/document/pdf/'
    img_url = 'dev/null'
    apiAddress = apiAddress
    proxyServer = proxyServer
    proxyAuth = proxyAuth

def proxyRequest(url,callback,meta={},headers={}):
    meta["proxy"] = proxyServer
    headers["Authorization"] = proxyAuth     
    time.sleep(1)  # random.randint(1,3)
    return scrapy.Request(url=url,meta=meta,callback=callback,headers=headers)

def matchPaper(item):
    print('----------post matchPaper--------------------------------------------------')
    data = {
        'author': item['author'],
        'keyword': item['keyword'],
        'title': item['title'],
    }
    url = apiAddress + '/paper/matchpaper'
    data = json.dumps(data)
    req = request.Request(url)  # 'http://localhost:9911'
    req.add_header('Content-Type', 'application/json')
    data = data.encode('utf-8')
    with request.urlopen(req, data=data) as f:
        # print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        value = f.read().decode('utf-8')

        value=json.loads(value)

        print('matchPaperData:', value)
        return value['data']


def savePaperPost(item, fileItem):  # 保存文章
    print('from spider download post------------------------------------------------------------')
    EmailArr = item['correspongdingauthorEmail'].split('||')
    email = ','.join(EmailArr)
    if len(EmailArr) == 2:
        email = email[:-1]

    keyword = item['keyword']
    if keyword == 'NULL':
        keyword = ''
    data = {
        "auditState": "WAIT",
        "author": item['author'],
        "correspondAuthorList": [
            {
                "email": email,
                "name": item['correspongdingauthor']
            }
        ],
        "doi": item['DOI'],

        "file": fileItem['mediaId'],
        "fileName": item['title'],
        "fileSize": fileItem['size'],

        "journalName": item['journalTitle'],
        "keyword": keyword,
        "origin": "COLLECT",
        "paperState": "SOLDOUT",
        "publishTime": item['publishTime'],
        "reelNumber": item['annualVolume'],
        "summary": item['abstract'],
        "title": item['title'],
    }
    print('---保存文献---------------------------------------------------------')
    print(data)
    print('------------------------------------------------------------------')

    url = apiAddress + '/paper'
    data = json.dumps(data)
    req = request.Request(url)  # 'http://localhost:9911'
    req.add_header('Content-Type', 'application/json')
    data = data.encode('utf-8')

    with request.urlopen(req, data=data) as f:
        # print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))


def postItemWithPdf(item):
    def dwnld(response):
        file_path = Config().pdf_url + response.meta['filename']
        if matchPaper(item) == True:
            print('已存在重复文献，跳过')
            return

        with open(file_path, 'wb') as f:  # 上传pdf文件
            f.write(response.body)
            print(
                '----------postItemWithPdf--------------------------------------------------')
            file = {'file': open(file_path, 'rb')}
            r = requests.post(apiAddress + '/paper/pdf', files=file)
            dic = json.loads(r.text)
            savePaperPost(item, dic['data']['media'])  # 保存文献信息
            if(os.path.exists(file_path)):  # 判断文件是否存在
                os.remove(file_path)
                print('移除文件：%s' % file_path)

    return dwnld


def postInPipeline(item):
    if item['pdf'] != 'NULL':
        print('----- pdf已存在----跳过Pipeline --------------------------------------------------')
        return
    
    print('------无pdf文件--postInPipeline--------------------------------------------------')

    if matchPaper(item) == True:
        print('已存在重复文献，跳过')
        return

    print('---post from pipeline-----------------------------------------------------------')
    correspongdingauthorEmail = item['correspongdingauthorEmail'].split('||')
    email = ','.join(correspongdingauthorEmail)
    keyword = item['keyword']
    if keyword == 'NULL':
        keyword = ''
    data = {
        "auditState": "WAIT",
        "author": item['author'],
        "correspondAuthorList": [
            {
                "email": email,
                "name": item['correspongdingauthor']
            }
        ],
        "doi": item['DOI'],

        # "file": fileItem['mediaId'],
        # "fileName": item['title'],
        # "fileSize": fileItem['size'],

        "journalName": item['journalTitle'],
        "keyword": keyword,
        "origin": "COLLECT",
        "paperState": "SOLDOUT",
        "publishTime": item['publishTime'],
        "reelNumber": item['annualVolume'],
        "summary": item['abstract'],
        "title": item['title'],
    }
    print('---pipeline post ---------------------------------------------------------')

    url = apiAddress + '/paper'
    data = json.dumps(data)
    req = request.Request(url)  # 'http://localhost:9911'
    req.add_header('Content-Type', 'application/json')
    data = data.encode('utf-8')

    with request.urlopen(req, data=data) as f:
        # print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))




