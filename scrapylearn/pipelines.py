# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from pymongo import MongoClient

class ScrapylearnPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonExportPipeline(object):
    def __init__(self):
        self.file = open("article.json", "wb")
        self.export = JsonItemExporter(self.file, ensure_ascii=False)
        self.export.start_exporting()

    def close_spider(self,spider):
        self.export.finish_exporting()
        self.file.close()
        print("close_spider")

    def process_item(self, item, spider):
        self.export.export_item(item)
        return item



class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item

class MongoDBPipeline(object):

    def __init__(self,db):
        self.db = db

    @classmethod
    def from_settings(cls,settings):
        dbparams=dict(
        host = settings["MONGODB_HOST"],
        port = settings["MONGODB_PORT"],
        username = settings["MONGODB_USER"],
        password = settings["MONGODB_PWD"],
        )
        dbase = settings["MONGODB_DBNAME"]
        conn = MongoClient(**dbparams)
        return cls(conn.dbase)


    def process_item(self, item, spider):
       self.db.article_detail.insert(item)
       return item

