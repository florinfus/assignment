import pandas as pd
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from furniture.spiders import FurnitureCrawler
from twisted.internet import reactor

urls = [urlparse(item).scheme + '://' + urlparse(item).netloc
        for item in pd.read_csv("../furniture stores pages.csv")['max(page)']]

runner = CrawlerRunner()
for url in urls[:2]:
    print(url)
   
    # process = CrawlerProcess(settings={
    #     'FEEDS': {f'results/{urlparse(url).netloc}_fulltext.csv': {'format': 'csv', 'overwrite': True}},
    #     'LOG_FILE': 'furniture_script_log.txt'
    # })
    # process.crawl(
    #     FurnitureCrawler.FurnitureCrawler,
    #     start_urls = [url]
    # )
    # process.start()
    # # process.start(stop_after_crawl=False)
    
    runner.settings['FEEDS'] = {f'results_fulltext_crawler/{urlparse(url).netloc}_fulltext.csv': {'format': 'csv', 'overwrite': True}}
    runner.settings['start_urls'] = [url]
    runner.settings['LOG_LEVEL'] = 'INFO'
    runner.settings['LOG_FILE'] = 'furniture_script_log.txt'
    runner.crawl(FurnitureCrawler.FurnitureCrawler)

d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()


