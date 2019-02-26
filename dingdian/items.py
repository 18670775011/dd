# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 书籍信息
class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_sid = scrapy.Field()
    book_name = scrapy.Field()
    book_auth = scrapy.Field()
    book_size = scrapy.Field()
    update_time = scrapy.Field()
    book_status = scrapy.Field()
    new_chapter = scrapy.Field()
    book_type = scrapy.Field()


# 书籍内容
class ContentItem(scrapy.Item):
    p_sid = scrapy.Field()
    p_name = scrapy.Field()
    chapter_title = scrapy.Field()
    chapter_content = scrapy.Field()
    sort_num = scrapy.Field()

