# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import cx_Oracle
from dingdian.items import DingdianItem, ContentItem


class DingdianPipeline(object):
    # pass
    def process_item(self, item, spider):
        # Oracle数据库连接
        # my_ora = cx_Oracle.connect('erms_book1/erms_book1@127.0.0.1/orcl')
        my_ora = pymysql.connect(host='localhost', port=3306, user='root', password='123456', charset='utf8', db='erms_xs', use_unicode=True)
        cur = my_ora.cursor()
        try:
            # 插入书籍信息到erms_book_info
            if isinstance(item, DingdianItem):
                print('书名：' + item['book_name'] + '------->>>正在存入数据库')
                cur.execute("insert into erms_book_info(id, book_name, book_auth, book_size, update_time, book_status, new_chapter, book_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (item['book_sid'], item['book_name'], item['book_auth'], item['book_size'], item['update_time'], item['book_status'], item['new_chapter'], item['book_type']))
				
            # 插入章节信息到erms_chapter_info
            elif isinstance(item, ContentItem):
                print('章节：' + item['chapter_title'] + '------->>>正在存入数据库')
                cur.execute('insert into erms_book_chapter(book_sid_id, chapter_title, chapter_content, book_name, sort_num) VALUES (%s, %s, %s, %s, %s )', (item['p_sid'], item['chapter_title'], item['chapter_content'], item['p_name'], item['sort_num']))
            my_ora.commit()
            cur.close()
            my_ora.close()
        except Exception as e:
            my_ora.commit()
            cur.close()
            my_ora.close()
            print("出现异常：", e)
        finally:
            return item
        # # 书籍内容
        # chapter_title = scrapy.Field()
        # chapter_content = scrapy.Field()

