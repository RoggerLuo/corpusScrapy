from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from PIL import Image
# from .settings import IMAGES_STORE as image_store
from qikan.config import Config
from qikan.fileWrite import write
class QikanPipeline(object):
    def __init__(self):
        self.engine = 'no'
    def process_item(self, item, spider):
        if item['download'] == True:
            # href = item['href']
            return 'end'
        print('-----PipelinePipelinePipelinePipeline------')
        title = item['title']
        data = item['content']
        path = os.path.join(Config().corpusPath,title + '.txt')
        write(path,data)
        return item

    def close_spider(self, spider):
        self.sess='no'

