import scrapy


class ReviewspiderSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']

    def parse(self, response):
        star_rating = response.xpath('//span[@class="a-icon-alt"]/text()').extract()
        comments = response.xpath('//span[@class="a-size-base review-text review-text-content"]/span/text()').extract()
        count = 0

        for item in zip(star_rating, comments):
            # создаем словарь для хранения собранной информации
            scraped_data = {
                'Рейтинг': item[0],
                'Отзыв': item[1],
            }

            next_page = response.css('.a-last a ::attr(href)').extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
            )
