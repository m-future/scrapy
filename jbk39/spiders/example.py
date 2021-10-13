import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['exasas.com']
    start_urls = ['http://exasas.com/']

    def parse(self, response):
        pass
