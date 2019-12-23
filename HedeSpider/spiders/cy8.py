import scrapy
import re
import datetime
import os
from bs4 import BeautifulSoup as bs
from HedeSpider import items, tools
import time
import uuid

class cy8_spider(scrapy.Spider):
    name = 'cy8'

    def __init__(self, *args, **kwargs):
        super(cy8_spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.cy8.com.cn/cyzcfg/']
        self.keywords = tools.reshape_kwargs(kwargs, 'keyword').split(',')
        self.userid = tools.reshape_kwargs(kwargs, 'userid')
        self.username = tools.reshape_kwargs(kwargs, 'username')
        self.taskid = tools.reshape_kwargs(kwargs, 'taskid')

    def parse(self, response):
        def days(day1, day2):
            day1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
            day2 = datetime.datetime.strptime(day2, '%Y-%m-%d')
            return (day2-day1).days

        url_re = re.compile(r'http://www.cy8.com.cn/cyzcfg/\d+')
        date_re = re.compile(r'\d{4}-\d{2}-\d{2}')

        for article in response.css('.con'):
            date_time = article.css('dd::text').get()
            if date_re.match(date_time) and days(date_time, datetime.datetime.now().strftime('%Y-%m-%d')) > 7:
                return
            href = article.css('a::attr(href)').get()
            if url_re.match(href):
                yield response.follow(href, self.parse_content)

        # for href in response.css('a.next::attr(href)'):
        #     yield response.follow(href, self.parse)

    def parse_content(self, response):
        title = response.css('.tit::text').get()
        if title is None:
            title = response.url
        # 防止文章标题出现非法字符
        title = tools.reshape_title(title)

        content = response.css('.content').get()
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
