from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from topliga.spiders.TopLiga import TopligaSpider
from topliga import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(TopligaSpider, brand='nike')#input('Choice a brand:'))
    process.start()
