BOT_NAME = "scrapy_code"
SPIDER_MODULES = ["dags.services.scrapy_code.spiders"]
NEWSPIDER_MODULE = "dags.services.scrapy_code.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "dags.services.scrapy_code.pipelines.ProductPipeline": 300,
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
