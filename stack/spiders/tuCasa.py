import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'tuCasa'
    allowed_domains = ['tucasa.com']
    start_urls = ['http://www.tucasa.com/alquiler/viviendas/barcelona/barcelona-capital/?r=&idz=0008.0001.9999.0001&p2=900&ord=&pgn=1']

    rules = (
        Rule (LinkExtractor(restrict_xpaths='//*[@id="container-tipo-listado"]/div[1]/div[24]/ul/li[11]/a'), follow= True),
        Rule (LinkExtractor(restrict_xpaths='//*[@class="divisor-tipo-listado col-xs-12"]//*[@class="div-btn-detalle"]/a'), callback = 'parse_items'),
    )
    
    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'tuCasa'
        item["url"]         = response.url
        item["title"]       = self.format_xpath(response, '/html/body/div[5]/h1/text()')
        item["price"]       = self.format_xpath(response, '/html/body/div[5]/div[1]/span[1]/text()').split()[0]
        item["update_date"] = self.format_xpath(response, '/html/body/div[6]/div/div[3]/span[2]/text()').split()[2]
        item["rooms"]       = self.format_xpath(response, '/html/body/div[6]/div/div[1]/ul/li[4]/text()').split()[0]
        item["surface"]     = self.format_xpath(response, '/html/body/div[6]/div/div[1]/ul/li[2]/span/text()').split()[0]
        item["location"]    = self.format_xpath(response, '/html/body/div[5]/span/text()')
        item["description"] = ''.join(response.xpath('/html/body/div[6]/div/div[1]/text()').extract()).strip()
        
        yield item
        
   
    def format_xpath(self, response, xpath):
        res = response.xpath(xpath)
        return res.extract()[0].encode('utf-8').strip() if res else ""