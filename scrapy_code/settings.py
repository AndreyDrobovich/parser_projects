BOT_NAME = "scrapy_code"
SPIDER_MODULES = ["scrapy_code.spiders"]
NEWSPIDER_MODULE = "scrapy_code.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "scrapy_code.pipelines.ProductPipeline": 300,
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
