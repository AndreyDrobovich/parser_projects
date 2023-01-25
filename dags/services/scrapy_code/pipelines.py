import csv
import json

from itemadapter import ItemAdapter


class ProductPipeline:
    def open_spider(self, spider):
        self.file = open("dags/services/scrapy_code/data/test.csv", "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Name", "Price", "Image"])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item.values())


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("data/flats.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
