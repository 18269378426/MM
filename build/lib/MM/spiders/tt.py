import scrapy
import logging
from datetime import datetime
from scrapy import Request
# from ..baseSpider import BaseSpider
from scrapy.spiders import CrawlSpider
import time

from MM.items import MmItem

class HcwangSpider(CrawlSpider):
    name = 'f'

    sourceName = '防城港天天网（本地资讯）'

    allowed_domains = ['bbs.guilinlife.com']

    qidian_headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
    }

    def start_requests(self):
        url = 'https://www.gxsky.com/thread-17242314-1-1.html'
        yield Request(url, headers=self.qidian_headers, callback = self.parse_item)

    def parse_item(self, response):
        # print(response.text)
        # item = self.createItem(response)
        item = MmItem()

        item['title'] =  response.css('#thread_subject::text').extract_first()

        item['postBy'] = response.css('.authi a::text').extract_first()


        postOn = response.css('.pti em')
        if postOn:
            # 发表于 xxx小时前
            postOn1 = postOn[0].css('span::attr(title)').extract_first()
            if not postOn1:

                arr1 = postOn[0].re(r"\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}")
                if arr1:
                    postOn1 = arr1[0]

            if postOn1:
                postOn = datetime.strptime(postOn1, '%Y-%m-%d %H:%M:%S')
        item['postOn'] = postOn


        item['text'] = ''.join(response.css('.t_f *::text').extract())

        yield item
