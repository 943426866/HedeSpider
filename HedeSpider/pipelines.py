# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from HedeSpider import tools
import time


class HedespiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=settings["MSSQL_HOST"],
            database=settings["MSSQL_DBNAME"],
            user=settings["MSSQL_USER"],
            password=settings["MSSQL_PASSWORD"],
            port=settings['MSSQL_PORT'],
            charset='utf8',
        )
        dbpool = adbapi.ConnectionPool("pymssql", **params)
        return cls(dbpool)

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addCallback(self.insert_callback, item)

    def insert_callback(self, result, item):
        if result == 1:
            tools.html2pdf(item['title'], item['content'], item['path'])

    def do_insert(self, cursor, item):
        insert_sql = "insert into T_Test2(title,path,userid) values(%s,%s,%s)"
        data = (item['title'], item['path'], item['userid'])
        try:
            cursor.execute(insert_sql, data)
            return 1
        except Exception as e:
            return 0
