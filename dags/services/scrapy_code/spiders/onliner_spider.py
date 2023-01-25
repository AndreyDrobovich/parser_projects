import scrapy
from dags.services.scrapy_code.configs.spider_mapping import DICT_MAPPING

from dags.services.scrapy_code.items import FlatItem


class FlatsSpider(scrapy.Spider):

    name = "flats"
    start_urls = [
        f"https://realt.by/sale/flats/?search=eJwryS%2FPi89LzE1VNXXKycwGUi5AlgGQslV1MVC1dAaRThZg0kXVxVDVwhDMdlSLL04tKS0AKi5KTY4vSC2KL0hMB2m3NTYAAAClF9o%3D"
    ]

    custom_settings = {"dags.services.scrapy_code.pipelines.ProductPipeline": False}

    def parse(self, response):

        max_page = int(
            response.xpath("//div[@class='paging-list']//a/text()").extract()[-1]
        )
        pages_links = [
            f"https://realt.by/sale/flats/?search=eJwryS%2FPi89LzE1VNXXKycwGUi5AlgGQslV1MVC1dAaRThZg0kXVxVDVwhDMdlSLL04tKS0AKi5KTY4vSC2KL0hMB2m3NTYAAAClF9o%3D&page={number}"
            for number in range(1, max_page)
        ]
        for link in pages_links:
            yield scrapy.Request(url=link, callback=self.append_flats)

    def append_flats(self, response):
        for link in response.xpath('//a[@class="image mb-0"]/@href').extract():
            yield scrapy.Request(url=link, callback=self.parse_flat_link)

    def parse_flat_link(self, response):
        item = FlatItem()
        item["images"] = response.xpath(
            '//img[@class="blur-sm scale-105"]/@src[contains(.,"https")]'
        ).extract()

        item["name"] = response.xpath("//section/h1/span/text()").extract()
        item["price_byn"] = response.xpath(
            '//div[@class="mt-0.5 mb-1.5"]/h2/text()'
        ).extract()[1]
        item["price_usd"] = response.xpath(
            '//div[@class="mt-0.5 mb-1.5"]/span/text()'
        ).extract()[2]
        full_adress = response.xpath(
            '//div[@class="md:-order-1 grow flex order-2 mb-6"]/ul/li/a/text()'
        ).extract()
        item["city"] = full_adress[0].replace("\xa0", "")
        item["adress"] = full_adress[1].replace("\xa0", "")
        item["metro"] = response.xpath("//div/ul/li/span/a/text()").extract()
        value_metrics = response.xpath(
            '//div[@class="flex flex-wrap md:justify-start -mt-6 md:mb-0 order-2 mb-6"]//div/text()'
        ).extract()
        name_metrics = response.xpath(
            '//div[@class="flex flex-wrap md:justify-start -mt-6 md:mb-0 order-2 mb-6"]/div//p/text()'
        ).extract()

        for number, name in enumerate(name_metrics):
            item[DICT_MAPPING[name]] = value_metrics[number]

        item["description"] = response.xpath(
            "//section[2]/div/div/div//p/text()"
        ).extract()
        yield item
