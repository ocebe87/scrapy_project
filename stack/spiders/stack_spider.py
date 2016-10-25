from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://www.vibbo.com/alquiler-de-pisos-barcelona-capital-particulares/?ca=8_s&m=8019&a=31&pe=900&fPos=210&fOn=sb_f_input",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//*[@id="hl"]/div')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'div/div[1]/div[2]/p[1]/a/text()').extract()
            item['url'] = question.xpath(
                'div/div[1]/div[2]/p[1]/a/@href').extract()
            item['price'] = question.xpath(
                'div/div[1]/div[2]/p[1]/a/@href').extract()
            yield item
