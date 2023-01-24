import csv


class ProductPipeline:
    def open_spider(self, spider):
        self.file = open("scrapy_code/data/test.csv", "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Name", "Price", "Image"])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item.values())
