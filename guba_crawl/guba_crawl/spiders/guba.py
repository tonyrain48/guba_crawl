# -*- coding: utf-8 -*-
import scrapy
from guba_crawl

class GubaSpider(scrapy.Spider):
    name = 'guba'
    allowed_domains = ['http://guba.eastmoney.com/']
    start_urls = ['http://http://guba.eastmoney.com//']

    pagenum_list=response.xpath('//span[@class="pagernums"]/@data-pager').extract()
    tiezi=response.xpath('//div[@class="articleh normal_post"]').extract()
    page=response.xpath('//span[@class="l3 a3"]/a/@href').extract()

    def parse(self, response):
        tiezi_list=response.xpath('//div[@class="articleh normal_post"]').extract()
        for tiezi in tiezi_list:
            tiezi_item=
        pass
