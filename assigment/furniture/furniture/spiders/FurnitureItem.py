import scrapy
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FurnitureItem1(scrapy.Spider):
    name = 'furniture_item1'
    start_urls = [
        'https://www.factorybuys.com.au/collections/furniture?page=' + str(i)
        for i in range(1, 76)
    ]
    custom_settings = {
        'FEEDS': {f'results_products/{urlparse(start_urls[0]).netloc}.csv': {'format': 'csv', 'overwrite': True}}
    }
    
    def parse(self, response):
        for product in response.css('div.card__information'):
            yield {
                'name': product.css('a.full-unstyled-link::text').get().strip(),
                # 'price': product.css('span.price-item--regular::text').get().strip().replace('$', ''),
                # 'link': product.css('a.full-unstyled-link').attrib['href'],
            }

class FurnitureItem2(CrawlSpider):
    name = 'furniture_item2'
    allowed_domains = ['lexiconhome.com']
    start_urls = ['https://lexiconhome.com/']
    custom_settings = {
        'FEEDS': {f'results_products/{urlparse(start_urls[0]).netloc}.csv': {'format': 'csv', 'overwrite': True}}
    }    
    rules = (
        Rule(LinkExtractor(allow='collections', deny='products')),
        Rule(LinkExtractor(allow='products'), callback='parse_product'),
    )
    
    def parse_product(self, response):
            yield {
                # 'name': response.css('p.garamond.h1::text').get().strip() # claytongrayhome.com
                # 'name': response.css('h1.product-title::text').get().strip() # bydesignmodern.com
                # 'name': response.css('h1.product-single__title::text').get().strip() # willowcreekteak.com
                # 'name': response.css('h2.product-single__title::text').get().strip() # mfdesign.com.my
                # 'name': response.css('h1::text').get().strip() # alteriors.ca
                # 'name': response.css('h1.product-single__title::text').get().strip() # mrnanyang.com
                # 'name': response.css('span.gf_product-title::text').get().strip() # welcometohome.com.au
                # 'name': response.css('h1.product_name::text').get().strip() # lavida-furniture.com
                'name': response.css('h1.:text').get().strip() # lexiconhome.com
            }