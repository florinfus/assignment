import pandas as pd
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FurnitureCrawler(CrawlSpider):
    name = 'furniture_crawler'
    # start_urls = [urlparse(item).scheme + '://' + urlparse(item).netloc
    #     for item in pd.read_csv("../furniture stores pages.csv")['max(page)']]
    start_urls = [
        'https://alteriors.ca/',
        'https://bydesignmodern.com/',
        'https://claytongrayhome.com/',
        'https://lavida-furniture.com/',
        'https://mrnanyang.com/',
        'https://welcometohome.com.au/',
        'https://www.mfdesign.com.my/',
        'https://www.willowcreekteak.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow='collections', deny='products')),
        Rule(LinkExtractor(allow='products'), callback='full_text'),
    )

    def full_text(self, response):
        text_list = set([
            item.strip()
            for item in response.xpath('//body//text()').extract()
            if len(item.strip()) and '\n' not in item.strip()
        ])
        # for item in text_list:
        #     yield {'names': item}
        pd.DataFrame(text_list).to_csv(
            f'results_fulltext_crawler/{urlparse(response.url).netloc}.csv',
            index=False, mode='a')