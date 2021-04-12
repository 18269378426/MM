import scrapy
# from ..baseSpider import BaseSpider
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from MM.items import MmItem


class Bbs25yzSpider(CrawlSpider):
    name = 'bbs_25yz'
    source_name = '宜州论坛（聚焦宜州）'
    allowed_domains = ['bbs.25yz.com']
    spider_tags = ['广西', '宜州', '论坛']
    start_urls = [
        'http://bbs.25yz.com/forum-24-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'http://bbs.25yz.com/thread-\d+-\d+-\d+.html')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

        if response.css('.alert_error p::text').extract():
            self.log('抱歉，指定的主题不存在或已被删除或正在被审核: ' + response.url, logging.INFO)
            super().dot_crawl_url(response.url)
            return None
        item = MmItem()

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.pi .authi .xw1::text').extract_first()

        item['postOn'] = response.css('.pti em::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}')[0] + ':00'

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item