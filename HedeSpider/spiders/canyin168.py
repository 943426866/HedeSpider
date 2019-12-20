import scrapy
import re
import datetime
import os
from bs4 import BeautifulSoup as bs
from HedeSpider import items, tools
import time


class canyin168_spider(scrapy.Spider):
    name = 'canyin168'

    def __init__(self, *args, **kwargs):
        super(canyin168_spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.canyin168.com/Article/']
        self.keywords = tools.reshape_kwargs(kwargs, 'keyword').split()
        self.userid = tools.reshape_kwargs(kwargs, 'userid')

    def parse(self, response):
        def days(day1, day2):
            day1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
            day2 = datetime.datetime.strptime(day2, '%Y-%m-%d')
            return (day2-day1).days

        # url_re = re.compile(r'http://www.canyin168.com/Article/xw/\d*.html')
        date_re = re.compile(r'\d{4}-\d{2}-\d{2}')

        for article in response.css('.article'):
            date_time = article.css('.article_date::text').get()
            if date_re.match(date_time) and days(date_time, datetime.datetime.now().strftime('%Y-%m-%d')) > 7:
                return
            href = article.css('a::attr(href)').get()
            if href is not None:
                yield response.follow(href, self.parse_content)

        for a in response.css('.pagecss a'):
            if a.css('::text').get() == '下一页':
                yield response.follow(a.css('::attr(href)').get(), self.parse)

    def parse_content(self, response):
        title = response.css('.biaoti h1 span font::text').get()
        if title is None:
            title = response.url
        # 防止文章标题出现非法字符
        title = tools.reshape_title(title)

        content = response.css('.zuo_nr').get()
        soup = bs(content, 'lxml')
        soup.find(class_='biaoti').extract()
        content = soup.prettify()
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
