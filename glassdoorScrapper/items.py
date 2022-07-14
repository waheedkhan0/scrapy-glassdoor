# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    requirements = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    job_status = scrapy.Field()
    timestamp = scrapy.Field()


class Test1Item(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    job_title = scrapy.Field()
    work_life_balance = scrapy.Field()
    location = scrapy.Field()
    time = scrapy.Field()
    pos = scrapy.Field()
    cons = scrapy.Field()
    advice = scrapy.Field()
    overal_rating = scrapy.Field()
    Culture_Values = scrapy.Field()
    Career_Opportunities = scrapy.Field()
    Comp_Benefits = scrapy.Field()
    Senior_Management = scrapy.Field()
