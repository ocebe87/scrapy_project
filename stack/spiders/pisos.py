import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'pisos'
    allowed_domains = ['pisos.com']
    start_urls = ['http://www.pisos.com/alquiler/pisos-barcelona_capital/hasta-900/']

    rules = (
        #Rule (LinkExtractor(restrict_xpaths='//*[@id="body"]/div[6]/div/div[1]/div[3]/ul/li[3]/span'), follow= True),
        Rule (LinkExtractor(restrict_xpaths='//*[@class="anuncioLink"]'), callback = 'parse_items'),
    )
        
    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'pisos'
        item["url"]         = response.url
        item["title"]       = self.format_xpath(response, '//*[@id="dvTitulo"]/div[1]/h1/text()')
        item["price"]       = self.format_xpath(response, '//*[@id="dvTitulo"]/div[2]/div[1]/div/div/span/text()').split()[0]
        #item["update_date"] = self.format_xpath(response, '//*[@class="gray-light size12"]/text()').split()[2]
        item["rooms"]       = self.format_xpath(response, '//*[@id="dvTitulo"]/div[1]/div[1]/div[2]/text()').split()[0]
        item["surface"]     = self.format_xpath(response, '//*[@id="dvTitulo"]/div[1]/div[1]/div[1]/text()').split()[0]
        #item["location"]    = self.format_xpath(response, '/html/body/div[5]/span/text()')
        item["description"] = ''.join(response.xpath('//*[@class="description"]/text()').extract()).strip()
        
        yield item
        
   
    def format_xpath(self, response, xpath):
        res = response.xpath(xpath)
        return res.extract()[0].strip() if res else ""