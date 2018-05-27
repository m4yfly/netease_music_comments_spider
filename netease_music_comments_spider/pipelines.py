# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from scrapy.exceptions import CloseSpider
import requests
from twisted.enterprise import adbapi

class MysqlTwistedPiple(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port = settings["MYSQL_PORT"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)           
        return item

    def handle_error(self, failure, item, spider):
        print (failure)

    def close_spider(self,spider):
        self.dbpool.close()


    def do_insert(self, cursor, item):
        try:
            insert_sql,params = item.get_insert_sql()
            cursor.execute(insert_sql,params)
        except Exception as e:
            print("insert failed:",e)
        else:
            print('insert success')
