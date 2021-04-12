import scrapy
from scrapy import Request

# from scrapy_redis.spiders import RedisSpider#导入RedisSpider
# scrapy.Spider

class NnSpider(scrapy.Spider):
    name = 'peopleliuyan'
    sourceName = '人民网留言'
    current_page = 1  # 记录当前页
    total_page = 0  # 总页数
    # allowed_domains = ['gxnews.com.cn']
    # start_urls = ['http://gxnews.com.cn/']

    def start_requests(self):
        url = ['http://liuyan.people.com.cn/forum/list?fid=282']
        for one_url in url:
            try:
                yield Request(one_url, callback=self.parse)
            except:
                print('不可以这样')

    #设计好请求头

    def parse(self, response):
        print(response.text)