import scrapy
import re
import datetime
import os
from bs4 import BeautifulSoup as bs
from HedeSpider import items, tools
import time
import uuid


class ebrun_spider(scrapy.Spider):
    name = 'ebrun'

    def __init__(self, *args, **kwargs):
        super(ebrun_spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.ebrun.com/o2o/catering/']
        self.keywords = tools.reshape_kwargs(kwargs, 'keyword').split(',')
        self.userid = tools.reshape_kwargs(kwargs, 'userid')
        self.username = tools.reshape_kwargs(kwargs, 'username')
        self.taskid = tools.reshape_kwargs(kwargs, 'taskid')

    def parse(self, response):
        def days(day1, day2):
            # 返回两个日期的差值
            day1 = datetime.datetime.strptime(day1, '%Y-%m-%d %H:%M')
            day2 = datetime.datetime.strptime(day2, '%Y-%m-%d')
            return (day2-day1).days

        date_re = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

        # 爬取当前页面上所有链接
        for article in response.css('.liebiao-item-xinwen'):
            date_time = article.css('.time::text').get()
            if date_re.match(date_time) and days(date_time, datetime.datetime.now().strftime('%Y-%m-%d')) > 7:
                return
            href = article.css('a:nth-child(1)::attr(href)').get()
            if href is not None:
                yield response.follow(href, self.parse_content)

        for href in response.css('.pagination-next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_content(self, response):
        title = response.css('.post-text-title::text').get()
        if title is None:
            title = response.url
        # 防止文章标题出现非法字符
        title = tools.reshape_title(title)

        content = response.css('.post-text').get()
        # 清除字体格式，图片
        content = tools.reshape_content(content)

        path = tools.reshape_path(self.name) 

        item = items.HedespiderItem()
        item['title'] = title
        item['content'] = content
        item['path'] = path
        item['userid'] = self.userid
        item['username'] = self.username
        item['taskid'] = self.taskid
        item['attachuuid'] = str(uuid.uuid4()).replace("-","")
        if len(self.keywords) == 0:
            yield item
        for keyword in self.keywords:
            if keyword in str(item):
                yield item
                break
