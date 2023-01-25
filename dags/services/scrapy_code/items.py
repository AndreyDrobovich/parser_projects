from itsdangerous import serializer
import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=str)
    image = scrapy.Field(serializer=str)


class FlatItem(scrapy.Item):
    images = scrapy.Field(serializer=list)
    name = scrapy.Field(serializer=str)
    price_byn = scrapy.Field(serializer=str)
    price_usd = scrapy.Field(serializer=str)
    city = scrapy.Field(serializer=str)
    adress = scrapy.Field(serializer=str)
    metro = scrapy.Field(serializer=str)
    main_area = scrapy.Field(serializer=str)
    living_area = scrapy.Field(serializer=str)
    floor = scrapy.Field(serializer=str)
    year = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=list)
    kitchen_area = scrapy.Field(serializer=str)
