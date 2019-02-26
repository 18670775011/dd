# -*- coding: utf-8 -*-
import scrapy
import re
from dingdian.items import DingdianItem, ContentItem
from bs4 import BeautifulSoup


class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['www.23us.so']
    start_urls = ['https://www.23us.so/']
    # 书籍ID
    b_id = 0


    # 获取所有类别的小说
    def parse(self, response):
        url_list = response.xpath('//div[@class="main m_menu"]/ul//li/a/@href').extract()
        # 遍历各个小说的分类
        for url in url_list:
            # if 'http' not in url and len(url) > 5:
            if 'full.html' in url:
                sub_url = 'https://www.23us.so' + url
                print(sub_url)
                yield scrapy.Request(url=sub_url, callback=self.get_book_info)

    # 获取各个类别的小说信息
    def get_book_info(self, response):
        item = DingdianItem()
        # 书名(以下获取的都是一个列表)
        book_names = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="L"][1]/a/text()').extract()
        # 最新章节
        new_chapter = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="L"][2]/a/text()').extract()
        # 作者
        book_auth = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="C"][1]/text()').extract()
        # 字数
        book_size = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="R"]/text()').extract()
        # 更新时间
        update_time = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="C"][2]/text()').extract()
        # 状态
        book_status = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="C"][3]/text()').extract()
        # 获取书籍的链接，进一步获取书籍的内容
        book_url = response.xpath('//*[@id="content"]//tr[@bgcolor="#FFFFFF"]//td[@class="L"][2]/a/@href').extract()
        # 获取小说的类型
        book_type = response.xpath('/html/head/title/text()').extract_first()[0:4]
        # 最新章节的链接其实是书籍的目录页面，获取该页面，从第一章开始翻页爬取

        for i in range(len(book_names)):
            self.b_id += 1
            book_name = book_names[i]
            item['book_sid'] = self.b_id
            item['book_name'] = book_name
            item['book_auth'] = book_auth[i]
            item['book_size'] = book_size[i]
            item['update_time'] = update_time[i]
            item['book_status'] = book_status[i]
            item['new_chapter'] = new_chapter[i]
            item['book_type'] = book_type
            url = book_url[i]
            yield item
            yield scrapy.Request(url=url, callback=self.chapter_info, meta={'book_sid': self.b_id, 'book_name': book_names[i]})
        # 下一页
        next_url = response.xpath('//*[@id="pagelink"]//a[@class="next"]/@href').extract_first()
        if next_url:
            # print('下一页：' + next_url)
            yield scrapy.Request(url=next_url, callback=self.get_book_info)
        else:
            print("小说爬取取完毕!!!")
            return 1

    # 获取章节信息
    def chapter_info(self, response):
        content_url = response.xpath('//*[@id="at"]//td[@class="L"]/a/@href').extract()
        # 章节排序
        sort_num = 0
        # 循环取出所有章节内容的url
        for url in content_url:
            # 章节顺序
            sort_num += 1
            yield scrapy.Request(url=url, callback=self.get_content, meta={'book_sid': response.meta['book_sid'],
                                                                           'book_name': response.meta['book_name'],
                                                                           'sort_num': sort_num})


    # 获取章节内容
    def get_content(self, response):
        item_c = ContentItem()
        item_c['p_sid'] = response.meta['book_sid']
        item_c['p_name'] = response.meta['book_name']
        item_c['sort_num'] = response.meta['sort_num']
        chapter_title = response.xpath('//*[@id="a_main"]/div[2]/dl/dd[1]/h1/text()').extract_first()
        content = BeautifulSoup(response.text, 'lxml').find('dd', id='contents').get_text()
        item_c['chapter_content'] = content
        item_c['chapter_title'] = chapter_title

        yield item_c



