import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=str)
    image = scrapy.Field(serializer=str)
