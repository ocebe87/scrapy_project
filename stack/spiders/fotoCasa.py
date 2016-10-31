import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'fotoCasa'
    allowed_domains = ['fotocasa.es']
    start_urls = ['http://www.fotocasa.es/alquiler/casas/barcelona-capital/listado-por-foto?crp=1&ts=barcelona%20capital&llm=724,9,8,232,376,8019,0,0,0&minp=0&maxp=800&opi=36&ftg=false&pgg=false&odg=false&fav=false&grad=false&fss=true&mode=1&cu=es-es&pbti=2&nhtti=3&craap=1&fss=true&fs=false']

    rules = (
        #Rule (LinkExtractor(restrict_xpaths='//*[@id="body"]/div[6]/div/div[1]/div[3]/ul/li[3]/span'), follow= True),
        Rule (LinkExtractor(restrict_xpaths='//a[starts-with(@id, "ctl00_content1_gridphotos_rptGridPhotos_ct")]'), callback = 'parse_items'),
    )
    
    
    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'fotocasa'
        item["url"]         = response.url
        item["rooms"]       = self.format_xpath(response, '//*[@id="litRooms"]/b/text()')
        item["surface"]     = self.format_xpath(response, '//*[@id="litSurface"]/b/text()')
        item["title"]       = self.format_xpath(response, '//*[@id="property-title"]/h1/text()')
        item["price"]       = self.format_xpath(response, '//*[@id="priceContainer"]/text()').split()[0]
        item["description"] = self.format_xpath(response, '//*[@id="ctl00_ddDescription"]/div[2]/p/text()')
        #item["location"]    = self.format_xpath(response, '/html/body/div[5]/span/text()')
        #item["update_date"] = self.format_xpath(response, '//*[@class="gray-light size12"]/text()').split()[2]
        
        yield item
        
   
    def format_xpath(self, response, xpath):
        res = response.xpath(xpath)
        return res.extract()[0].strip() if res else ""