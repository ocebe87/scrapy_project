import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'yaEncontre'
    allowed_domains = ['yaencontre.com']
    start_urls = ['http://www.yaencontre.com/alquiler/viviendas/barcelona/f--900-euros/o-created_at,desc']

    rules = (
        #Rule (LinkExtractor(restrict_xpaths='//*[@id="body"]/div[6]/div/div[1]/div[3]/ul/li[3]/span'), follow= True),
        Rule (LinkExtractor(restrict_xpaths='//*[starts-with(@id, "inm_")]'), callback = 'parse_items'),
    )
    
    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'yaEncontre'
        item["url"]         = response.url
        item["rooms"]       = self.format_xpath(response, '//*[@id="main-content"]/div[1]/div[1]/div/p/text()[3]').split()[0]
        item["surface"]     = self.format_xpath(response, '//*[@id="main-content"]/div[1]/div[1]/div/p/text()[1]').split()[0]
        item["title"]       = self.format_xpath(response, '//*[@id="main-content"]/div[1]/div[1]/h1/text()')
        item["price"]       = self.format_xpath(response, '//*[@id="main-content"]/div[3]/div[3]/div[1]/p/span/text()').split()[0]
        item["description"] = ''.join(response.xpath('//*[@id="description"]/div/p').extract()).strip()
        #item["location"]    = self.format_xpath(response, '/html/body/div[5]/span/text()')
        #item["update_date"] = self.format_xpath(response, '//*[@class="gray-light size12"]/text()').split()[2]
        
        yield item
        
   
    def format_xpath(self, response, xpath):
        res = response.xpath(xpath)
        return res.extract()[0].strip() if res else ""