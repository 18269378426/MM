import scrapy
# from ..baseSpider import BaseSpider
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from MM.items import MmItem


class GxbsbSpider(CrawlSpider):
    name = 'gxbs'
    source_name = '右江论坛'
    allowed_domains = ['bbs.gxbs.net']
    spider_tags = ['广西', '百色', '论坛']
    start_urls = [
        'http://bg.gxbs.net/',
        'http://xy.gxbs.net/',
        'http://bbs.gxbs.net/thread-htm-fid-312.html',
        'http://bbs.gxbs.net/thread-htm-fid-311.html',
        'http://bbs.gxbs.net/thread-htm-fid-304.html',
        'http://bbs.gxbs.net/thread-htm-fid-313.html',
        'http://bbs.gxbs.net/thread-htm-fid-308.html',
        'http://bbs.gxbs.net/thread-htm-fid-305.html',
        'http://bbs.gxbs.net/thread-htm-fid-303.html',
        'http://bbs.gxbs.net/thread-htm-fid-306.html',
        'http://bbs.gxbs.net/thread-htm-fid-307.html',
        'http://bbs.gxbs.net/thread-htm-fid-309.html',
        'http://bbs.gxbs.net/thread-htm-fid-310.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'read-htm-tid-\d+.html')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

        item = MmItem()

        item['title'] = response.css('.read_h1::text').extract_first()

        taskName = response.css('.userCard.face_img.ddaxs img::attr(src)').extract_first()
        if str(taskName)[:4] != 'http':
            taskName = "http://bbs2.gxbs.net/" + taskName
        item['taskName'] = taskName

        item['postBy'] = response.css('.f14::text').extract_first()

        item['postOn'] = response.css('.fr span::attr(title)').extract_first()



        return item
