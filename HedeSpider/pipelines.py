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
            tools.html2pdf(item['title'], item['content'], item['path'], item['attachuuid'])

    def do_insert(self, cursor, item):
        print(item['attachuuid'])
        format_string = "%Y-%m-%d %H:%M:%S"
        time_array = time.localtime(time.time())
        str_date = time.strftime(format_string, time_array)
        print(str_date)
        dataDoc = (0, item['title'], ' ', item['title'], 'python爬取', item['userid'], item['username'], str_date,
                   str_date, item['attachuuid'], 0, 0, 0, 0, 0, 0, '01', '04', 0, 0, 0, 0, 0, 0, 0, '01', '01', 2)
        update_crawlSuccess = "update T_Bus_CrawlTask set taskstatus = '03',enddate = %s,crawnum = crawnum + 1 where taskid = %s"
        dataCrawl = (str_date,item['taskid'])
        try:
            cursor.callproc("P_Save_DocumentBase", dataDoc)
            cursor.execute(update_crawlSuccess, dataCrawl)
            return 1
        except Exception as e:
            return 0
