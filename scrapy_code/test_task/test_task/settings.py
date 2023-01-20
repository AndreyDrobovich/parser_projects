BOT_NAME = 'test_task'
SPIDER_MODULES = ['test_task.spiders']
NEWSPIDER_MODULE = 'test_task.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
   'test_task.pipelines.ProductPipeline': 300,
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
