import scrapy
from scrapy import Request
from MM.items import MmItem
from scrapy_redis.spiders import RedisSpider#导入RedisSpider
# scrapy.Spider
class NnSpider(RedisSpider):
    name = 'MM'
    current_page = 1   #记录当前页
    total_page = 0     #总页数
    allowed_domains = ['bbs.guilinlife.com']
    #start_urls = ['http://bbs.guilinlife.com/']
    # qidian_headers = {
    #
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
    # }
    # def start_requests(self):
    #     url = 'http://bbs.guilinlife.com/forum-323-1.html'
    #     yield Request(url, headers=self.qidian_headers, callback=self.parse)
    # #设计好请求头
    def parse(self, response):
        list_selector = response.xpath("//form[@method='post']/table[@summary='forum_323']/tbody")
        print(len(list_selector))
        for one_selecotr in list_selector:
            try:
                #获取标题

                title = one_selecotr.xpath("tr/th/a[@class='s xst']/text()").extract_first()
                # print(title)

                author = one_selecotr.xpath("tr/td[@class='by']/cite/a/text()").extract_first()
                # print(author)
                url = 'http://bbs.guilinlife.com/' + one_selecotr.xpath("tr/th/a[@class='s xst']/@href").extract_first()
                # print(url)

                item = MmItem()
                item['title'] = title

                item['url'] = url

                item['author'] = author
                yield Request(url,
                            meta={"item": item},
                            callback=self.property_parse)
            except:
                print("NULL")

        # 获取下一页URL，并生成Request请求
        # （1）获取下一页URL。仅在解析第一页时获取总页数的值
        if self.current_page == 1:
            # 属性page-data的值中包含总页数和当前页。
            self.total_page = response.xpath("//span[@id='fd_page_top']//a/text()").re("\d+")
            self.total_page = int(self.total_page[0])
        self.current_page += 1  # 下一页的值
        if self.current_page<=2:  #self.total_page:#判断页数是否已越界
            next_url = "http://bbs.guilinlife.com/forum.php?mod=forumdisplay&fid=323&page=%d"%(self.current_page)
            #（2）根据URL生成Request，使用yield提交给引擎            yield Request(next_url)
    # 详细页解析函数
    def property_parse(self, response):
        # 1.提取房屋产权信息ize-space(.)]").extract()#加[0]或者extract_first()都没有信息
        list3 = response.selector.xpath(
            "//div[@id='first']//div[@class='t_fsz']//td[@class='t_f']//text()[normalize-space(.)]").extract()
        # 2.获取主页面中的信息
        content = ' '.join(list3).replace('\n', '').replace('\r', '')
        # print(content)
        # print(content)

        item = response.meta["item"]
        item["content"] = content
        #list = response.xpath("//div[@class='comeing_viewthread']/div[@class='comeing_viewthread_r']")
        #print(len(list))
        review = response.selector.xpath(
            "//div[@class='comeing_viewthread']/div[@class='comeing_viewthread_r']//td[@class='t_f']  // text()[normalize-space(.)]").extract()
        #print(review)
        review_r = response.selector.xpath(
            "//div[@class='comeing_viewthread']/div[@class='comeing_viewthread_r']//td[@rowspan='2']/div/div[@class='pi']/div[@class='authi']/a/text()").extract()

        date = response.selector.xpath(
            "//div[@class='comeing_viewthread']/div[@class='comeing_viewthread_r']//div[@class='pti']/div[@class='authi']/em//text()").extract()
        for one_reviw_r in review_r:
            # print(one_reviw_r)
            one_reviw_r = one_reviw_r
        for one_date in date:
            # print(one_date)
            one_date = one_date
            one_date = one_date.replace('\n', '').replace('\r', '')
        for one_reviw in review:
            # print(one_reviw)
            one_reviw = one_reviw
            one_reviw = one_reviw.replace('\n', '').replace('\r', '')
        review_New = '最新评论人:' + one_reviw_r + '  ' + '评论时间:'+ one_date + '   ' + '评论内容:'+ one_reviw#先指明一下这里的用意虽然是循环，但是遍历后只要了最后一个评论人的消息，也就达到了每次刷新或者有消息进来保证取到了最新评论
        # item = response.meta["item"]

        item["review_New"] = review_New



        #发表时间
        date = vars()
        yield item



