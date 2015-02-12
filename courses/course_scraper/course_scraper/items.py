# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Course(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    periodo = scrapy.Field()
    link = scrapy.Field()
    starts = scrapy.Field()
    finishes = scrapy.Field()
    duration = scrapy.Field()
    type = scrapy.Field()
    assessments = scrapy.Field()
    credentialing = scrapy.Field()
    credit = scrapy.Field()
    level = scrapy.Field()
    university = scrapy.Field()
    url = scrapy.Field()
    weeks =  scrapy.Field()
    hpw = scrapy.Field()


