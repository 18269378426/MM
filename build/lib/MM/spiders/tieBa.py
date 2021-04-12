from scrapy.spiders import CrawlSpider
import scrapy
import re
from MM.items import MmItem

class BaiduTiebaSpider(CrawlSpider):
    name = 'baidu_tieba'
    source_name = '百度贴吧'
    allowed_domains = ['tieba.baidu.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
    }
    start_urls = ['https://tieba.baidu.com/f?kw=广西大学']

    spider_tags = ['广西', '贴吧', '高校']

    def _parse(self, response, **kwargs):
        results = re.findall(r'<a rel="noreferrer" href="(/p/\d+)" title="(\S+)"', response.body.decode())
        for url,title in results:
            yield scrapy.Request('https://tieba.baidu.com' +url, callback=self.parse_item)

    def parse_item(self, response):

        item = MmItem()
        item['postOn'] = ''
        item['postBy'] = response.css('.d_name ::text').extract()[1]
        item['title'] = response.css('.core_title_txt ::text').extract_first()
        item['taskName'] = response.css('.p_author_face img::attr(src)').extract_first()
        item['text'] = '\n'.join([x.strip() for x in response.xpath('//div[@id and contains(@id,"post_content_")]').css(
            '*::text').extract()])
        if len(item['title']) == 0:
            self.error('error: 获取不到帖子标题,' + response.url)
            return None
        return item
