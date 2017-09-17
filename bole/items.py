# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    head = scrapy.Field()
    post_time = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    vote_num = scrapy.Field()
    comment_num = scrapy.Field()
    collection_num = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()


