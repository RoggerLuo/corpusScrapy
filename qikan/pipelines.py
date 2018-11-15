from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from PIL import Image
# from .settings import IMAGES_STORE as image_store
from qikan.config import postInPipeline

class QikanPipeline(object):
    def __init__(self):
        self.engine = 'no'
    def process_item(self, item, spider):
        postInPipeline(item)
        return item

    def close_spider(self, spider):
        self.sess='no'

