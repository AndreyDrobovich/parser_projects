import scrapy


class ReviewspiderSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ['ab.onliner.by']
    start_urls = ['https://ab.onliner.by/']

    def parse(self, response):
        avto = response.xpath('//span[@class="a-icon-alt"]/text()').extract()
        year = response.xpath('//span[@class="a-size-base review-text review-text-content"]/span/text()').extract()

        for item in zip(star_rating, comments):
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
