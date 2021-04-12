# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem

from scrapy import Item

class MmPipeline(object):
    def __init__(self):
        self.url_set = set()
    def process_item(self, item, spider):
        if item['url'] in self.url_set:
            # 抛弃重复的Item项
            raise DropItem('查找到重复链接的项目：%s'%item)
        else:
            self.url_set.add(item['url'])
        return item


import json
from kafka import KafkaProducer, producer
from itemadapter import ItemAdapter
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

import logging
import types
import re
import pytz

tz = pytz.timezone('Asia/Shanghai')
class ConvertPostOnPipeline(object):

    def __init__(self) -> None:
        self.logger = logging.getLogger('ConvertPostOnPipeline')

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            if 'postOn' in item and item['postOn'] and isinstance(item['postOn'], str):
                try:
                    item['postOn'] = datetime.strptime(
                        item['postOn'].strip(), '%Y-%m-%d %H:%M:%S').astimezone(tz)
                except:
                    self.logger.error('error postOn: %s,%s ', item['postOn'], item['url'])
                    item['postOn'] = datetime.now(tz=tz)
            elif 'postOn' in item and item['postOn'] and isinstance(item['postOn'], datetime):
                item['postOn'] = item['postOn'].astimezone(tz=tz)
            else:
                item['postOn'] = datetime.now(tz=tz)

            return item


class ClearTextPipeline(object):
    pattern = re.compile(r"[\x00-\x1f\x7f ]")

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            if item['text']:
                item['text'] = self.clearText(item)
            item['title'] = (item['title'] or '').strip()

            return item

    def clearText(self, item):

        text = '\n'.join(item['text']) if isinstance(
            item, types.GeneratorType) or isinstance(item, list) else item['text']
        text.replace('\t', '').replace('\n', '').replace('\r', '').replace('\u3000','').replace(' ','')
        text = re.sub(self.pattern, '', text)
        return text
import pymongo
class MongoDBPipeline(object):
    #Spider开启时，获取数据库配置信息，连接MongoDB数据库服务器
    def open_spider(self,spider):
        #获取配置文件中MongoDB配置信息
        host = spider.settings.get("MONGODB_HOST","localhost")#主机地址
        port = spider.settings.get("MONGODB_PORT",27017)#端口
        db_name = spider.settings.get("MONGODB_NAME","LUNTAN")#数据库名称
        collection_name = spider.settings.get("MONGODB_COLLECTION","shuju")#集合名称
        #连接MongoDB，得到一个客户端对象
        self.db_client = pymongo.MongoClient(host=host, port=port)
        self.db_client = pymongo.MongoClient('mongodb://localhost:27017/')
        #指定数据库,得到一个数据库对象
        self.db = self.db_client[db_name]
        #指定集合，得到一个集合对象
        self.db_collection = self.db[collection_name]


    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
        self.db_collection.insert_one(item)

    # 关闭数据库
    def close_spider(self, spider):
        self.db_client.close()
class KafkaPipeline(object):
    settings = None
    producer = None
    topic = 'bbs'

    def __init__(self):
        self.logger = logging.getLogger('KafkaPipeline')

    def __del__(self):
        self.producer.close()

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        ext.producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip', value_serializer=lambda v: json.dumps(dict(v), default=str).encode('utf-8')) #重点
        return ext

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            self.send_item(item)
            return item

    def send_item(self, item):
        self.logger.info('send item {postBy},{title}'.format(**{
            'postBy': item['postBy'],
            'title': item['title'],
            # 'url': item['url'],
        }))
        self.producer.send(self.topic, value=item)

    def close_spider(self, spider):
        pass
