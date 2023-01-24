import scrapy
from dags.services.scrapy_code.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        "https://www.petsonic.com/farmacia-para-gatos/?p=%s" % page
        for page in range(1, 11)
    ]
    number = 1

    def parse(self, response):

        product_links = response.xpath(
            '//div[@class="product-desc display_sd"]/a/@href'
        ).extract()
        for link in product_links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):
        name = response.xpath('//p[@class="product_main_name"]/text()').extract()
        count_list = response.xpath(
            '//div[@class="attribute_list"]//span[@class="radio_label"]/text()'
        ).extract()
        price_list = response.xpath(
            '//div[@class="attribute_list"]//span[@class="price_comb"]/text()'
        ).extract()
        link_image = response.xpath('//*[@id="bigpic"]/@src').extract()

        for num, value in enumerate(count_list):
            item = {
                "name": f"{name[0]} {value}",
                "price": price_list[num],
                "image": link_image[0],
            }
            yield ProductItem(
                name=item["name"], price=item["price"], image=item["image"]
            )
