import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'enAlquiler'
    allowed_domains = ['enalquiler.com']
    start_urls = ['http://www.enalquiler.com/search?provincia=9&poblacion=4596&precio_max=900&tipo_usuario=1']

    rules = (
        Rule (LinkExtractor(restrict_xpaths='//*[@id="body"]/div[6]/div/div[1]/div[3]/ul/li[3]/span'), follow= True),
        Rule (LinkExtractor(restrict_xpaths='//*[@class="property-title"]'), process_links='link_filtering', callback = 'parse_items'),
    )
    
    def link_filtering(self, links):
        ret = []
        for link in links:
            sep='.html'
            link.url = link.url.split(sep, 1)[0] + sep
        return links
        
    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'enAlquiler'
        item["url"]         = response.url
        item["title"]       = self.format_xpath(response, '//*[@class="detail-name"]/text()')
        item["price"]       = self.format_xpath(response, '//*[@class="detail-price"]/text()')[:-1]
        #item["price"]       = '---'
        item["update_date"] = self.format_xpath(response, '//*[@class="gray-light size12"]/text()').split()[2]
        item["rooms"]       = self.format_xpath(response, '//*[@class="detail-rooms"]/text()').split()[0]
        item["surface"]     = self.format_xpath(response, '//*[@class="detail-m2"]/text()')[:-1]
        #item["location"]    = self.format_xpath(response, '/html/body/div[5]/span/text()')
        item["description"] = ''.join(response.xpath('//*[@id="description"]/text()').extract()).strip()
        
        yield item
  
    def format_xpath(self, response, xpath):
        res = response.xpath(xpath)
        return res.extract()[0].encode('utf-8').strip() if res else ""