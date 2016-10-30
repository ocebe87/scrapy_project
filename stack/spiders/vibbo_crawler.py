import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'vibbo_crawler'
    allowed_domains = ['vibbo.com']
    start_urls = ['http://www.vibbo.com/alquiler-de-pisos-barcelona-capital-particulares/?ca=8_s&m=8019&a=31&pe=900&fPos=210&fOn=sb_f_input']

    rules = (
        Rule (LinkExtractor(restrict_xpaths='//*[@id="result_container"]/div/div[2]/a[3]'), follow= True),
        Rule (LinkExtractor(restrict_xpaths='//*[@id="hl"]//*[@class="thumbnail_container"]'), callback = 'parse_items'),
    )

    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'vibbo'
        item["url"]         = response.url
        item["title"]       = response.xpath('//*[@id="main"]/div[1]/div/div[4]/div/div[1]/h1/text()').extract()[0].strip()
        item["price"]       = re.sub(r'[^\w]', '',response.xpath('//*[@id="main"]/div[1]/div/div[4]/div/div[1]/div/div/div[1]/span/text()').extract()[0].strip())
        item["update_date"] = response.xpath('//*[@id="main"]/div[1]/div/div[5]/div/div[3]/div/text()').extract()[0].strip()
        item["features"]    = map(unicode.strip,response.xpath('//*[@id="main"]/div[1]/div/div[5]/div/div[2]/ul/li/text()').extract())
        item["description"] = response.xpath('//*[@id="descriptionText"]/text()').extract()[1]
        item["rooms"]       = response.xpath('//*[@id="main"]/div[1]/div/div[5]/div/div[1]/div[1]/span/b/text()').extract()[0].strip()
        item["surface"]     = response.xpath('//*[@id="main"]/div[1]/div/div[5]/div/div[1]/div[2]/span/b/text()').extract()[0].strip()
        item["images"]      = response.xpath('//*[@id="slides"]//@src').extract()
        item["location"]    = response.xpath('//*[@id="main"]/div[1]/div/div[4]/div/div[3]/div[1]/span[2]/text()').extract()[0].strip()
        item["postal_code"] = response.xpath('//*[@id="main"]/div[1]/div/div[4]/div/div[3]/div[1]/span[3]/text()').extract()[0].strip()
        
        yield item
