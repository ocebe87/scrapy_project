import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class VibboCrawlerSpider(CrawlSpider):
    name = 'habitaclia'
    allowed_domains = ['habitaclia.com']
    start_urls = ['http://www.habitaclia.com/alquiler-barcelona.htm?tip_op_origen=A&pmax=900&m2=0&st=piso-estudio-apartamento-planta_baja-loft-duplex-triplex-atico-casa-torre-masia-casa_pareada-casa_adosada-chalet&hab=99&bolIsFiltro=1&hUserClickFilterButton=true&filtro_periodo=0&hMinLat=&hMinLon=&hMaxLat=&hMaxLon=&hUseLatLonFilters=&hNumPointsMapa=&ordenar=fec_mod_desc']

    rules = (
        #Rule (LinkExtractor(restrict_xpaths='//*[@class="siguiente"]'), process_links='link_filtering', follow= True),
        Rule (LinkExtractor(restrict_xpaths='//*[@id="listaAds"]/ul/li//*[@class="datos"]/h3/a'), callback = 'parse_items'),
    )
    
    def parse_items(self, response):
        item = StackItem()
        item["company"]     = 'habitaclia'
        item["url"]         = response.url
        item["title"]       = self.format_xpath(response, '//*[@class="h1ficha"]/text()')
        item["price"]       = self.format_xpath(response, '//*[@class="precio-ficha"]/span/text()').split()[0]
        item["detailReference"] = self.format_xpath(response, '//*[@class="referencia-ficha"]/span/text()')
        item["rooms"]       = ""
        item["surface"]       = ""
        #item["update_date"] = self.format_xpath(response, '//*[@id="contents_n"]/div[4]/div/div[1]/span/text()').split()[4].replace("(","").replace(")","")
        #item["rooms"]       = self.format_xpath(response, '//*[@class="detail-rooms"]/text()').split()[0]
        #item["surface"]     = self.format_xpath(response, '//*[@class="detail-m2"]/text()')[:-1]
        #item["location"]    = self.format_xpath(response, '/html/body/div[5]/span/text()')
        #item["description"] = ''.join(response.xpath('//*[@id="description"]/text()').extract()).strip()
        
        yield item
        
   
    def format_xpath(self, response, xpath):
        res = response.xpath(xpath)
        return res.extract()[0].encode('utf-8').strip() if res else ""