import scrapy
# from ..baseSpider import BaseSpider
from scrapy.spiders import CrawlSpider
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from MM.items import MmItem

class Lstc03Spider(CrawlSpider):
    name = 'lstc03'
    source_name = '灵山同城网（网友爆料）'
    allowed_domains = ['www.03tc.com']
    spider_tags = ['广西', '灵山', '论坛']
    start_urls = [
        'http://www.03tc.com/forum.php?mod=forumdisplay&fid=62',
    ]
    rules = [Rule(LinkExtractor(allow=(r'forum.php\?mod=viewthread&tid=\d+&extra=page%3D1')), callback='parse_item', follow=False)
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

        postOn = response.css('.pti em')
        if postOn:
            # 发表于 xxx小时前
            postOn1 = postOn[0].css('span::attr(title)').extract_first()
            if not postOn1:

                arr1 = postOn[0].re(r"\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}")
                if arr1:
                    postOn1 = arr1[0]

            if postOn1:
                item['postOn'] = datetime.strptime(postOn1, '%Y-%m-%d %H:%M:%S')

        # item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item