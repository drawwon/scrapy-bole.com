# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import os
import MySQLdb
import codecs
import json
from twisted.enterprise import adbapi
# import MySQLdb.cursors

class BolePipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', password='123456',
                                    database='scrapy', port=3306,charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO article (head, post_time, url, url_id) VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['head'],item['post_time'],item['url'],item['url_id']))
        self.conn.commit()

class twisted_mysql_pipelines(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparm = dict(host=settings['MYSQL_HOST'],
                      user=settings['MYSQL_USER'],
                      password=settings['MYSQL_PASSWORD'],
                      database=settings['MYSQL_DBNAME'],
                      cursorclass = MySQLdb.cursors.DictCursor,
                      charset='utf8',
                      use_unicode=True)
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparm)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.error_handler)#处理异常

    def error_handler(self, error):
        print(error)

    def do_insert(self, cursor, item):
        insert_sql = """
                    INSERT INTO article (head, post_time, url, url_id) VALUES (%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (item['head'], item['post_time'], item['url'], item['url_id']))





class MyjsonPipelines(object):
    #自定义的json导出
    def __init__(self):
        self.file = codecs.open('myarticle.json', mode='w', encoding='utf8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(line)
        return item
    def spider_close(self,spider):
        self.file.close()

class jsonPipelines(JsonItemExporter):
    #调用scrapy提供的json exporter来导出json文件
    def __init__(self):
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf8', ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class articleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value['path']
            item['front_image_path'] = os.path.abspath(image_file_path)
        return item