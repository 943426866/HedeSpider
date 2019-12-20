import scrapy
import re
import datetime
import os
from bs4 import BeautifulSoup as bs
from HedeSpider import items, tools
import time


class techfood_spider(scrapy.Spider):
    name = 'tech-food'

    def __init__(self, *args, **kwargs):
        super(techfood_spider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.tech-food.com/news/series/1301/list.html']
        self.keywords = tools.reshape_kwargs(kwargs, 'keyword').split()
        self.userid = tools.reshape_kwargs(kwargs, 'userid')

    def parse(self, response):
        def days(day1, day2):
            # 返回两个日期的差值
            day1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
            day2 = datetime.datetime.strptime(day2, '%Y-%m-%d')
            return (day2-day1).days

        date_re = re.compile(r'\d{4}-\d{2}-\d{2}')

        # 爬取当前页面上所有链接
        for article in response.css('.titleTxt'):
            date_time = article.css('.timeTxt::text').get()
            if date_re.match(date_time) and days(date_time, datetime.datetime.now().strftime('%Y-%m-%d')) > 7:
                return
            href = article.css('a::attr(href)').get()
            if href is not None:
                yield response.follow(href, self.parse_content)

    def parse_content(self, response):
        title = response.css('h1::text').get()
        if title is None:
            title = response.url
        # 防止文章标题出现非法字符
        title = tools.reshape_title(title)

        content = response.css('#zoom').get()
        # 清除字体格式，图片
        content = tools.reshape_content(content)

        path = tools.reshape_path(self.name)

        item = items.HedespiderItem()
        item['title'] = title
        item['content'] = content
        item['path'] = path
        item['userid'] = self.userid
        if len(self.keywords) == 0:
            yield item
        for keyword in self.keywords:
            if keyword in str(item):
                yield item
                break
