# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    review_New = scrapy.Field()
    date = scrapy.Field()
    id = scrapy.Field()

    crawlOn = scrapy.Field()
    postOn = scrapy.Field()
    postBy = scrapy.Field()
    source = scrapy.Field()
    spider = scrapy.Field()
    taskName = scrapy.Field()
    text = scrapy.Field()
    html = scrapy.Field()
    spiderTags = scrapy.Field()
    tags = scrapy.Field()
