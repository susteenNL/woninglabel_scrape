from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('woninglabel_business')
process.start() # the script will block here until the crawling is finishe