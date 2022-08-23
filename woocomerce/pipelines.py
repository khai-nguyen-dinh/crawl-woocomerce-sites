# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

import requests
from scrapy import signals, Request
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline

from woocomerce.settings import FEED_EXPORT_FIELDS


class WoocomercePipeline:

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('data/' + spider.name + '.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = FEED_EXPORT_FIELDS
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        sha1_and_extension = request.url.split('/')[-1]
        return request.meta.get('filename', '') + 'img/' + sha1_and_extension

    def get_media_requests(self, item, info):
        for image in item['all_image']:
            yield Request(image)


class UpdateLinkPipeline(object):
    def process_item(self, item, spider):
        thumbnail = []
        if item['images']:
            for image in item['images']:
                thumbnail.append('img/' + image.split('/')[-1])
        item['images'] = thumbnail
        description = []
        if type(item['description']) is list:
            for image in item['description']:
                description.append('img/' + image.split('/')[-1])
        item['description'] = description
        return item
