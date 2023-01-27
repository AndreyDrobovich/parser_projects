from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from services.scrapy_code.spiders.onliner_spider import FlatsSpider
from services.scrapy_code import settings as my_settings


class FlatsFunctions:
    def process_spider():
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(FlatsSpider)
        process.start()
