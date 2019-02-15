# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import MySQLdb
import redis
from scrapy import Item


class SQLlitePipeline(object):
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'demo.db')
        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        insert_data = 'INSERT INTO books VALUES(?,?,?,?,?,?)'

        self.db_cur.execute(insert_data, values)


class MySQLPipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '12345')
        self.db_conn = MySQLdb.connect(
            host=host, port=port, db=db,
            user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        insert_data = 'INSERT INTO books VALUES(%s,%s,%s,%s,%s,%s)'

        self.db_cur.execute(insert_data, values)


class RedisPipeline(object):
    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 6379)
        db_index = spider.settings.get('REDIS_INDEX', 0)
        db_password = spider.settings.get('REDIS_PASSWORD', 'ab12')
        self.db_conn = redis.StrictRedis(
            host=db_host, port=db_port, db=db_index, password=db_password)
        self.item_i = 0

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        item = dict(item)
        self.item_i += 1
        self.db_conn.hmset('book:%s' % self.item_i, item)
