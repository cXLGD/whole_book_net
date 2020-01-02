# -*- coding: utf-8 -*-
import scrapy
from ..items import QuanshuwangSpiderItem


class QuanshuwwangSpider(scrapy.Spider):
    name = 'quanshuwwang'
    # allowed_domains = ['ddddd']
    start_urls = ['http://www.quanshuwang.com/']

    def parse(self, response):
        category_url_list = response.xpath('//ul[@class="channel-nav-list"]//a/@href').extract()
        for i in category_url_list:
            yield scrapy.Request(i,callback=self.detail_parse)

    def detail_parse(self,response):
        title_list = response.xpath('//ul[@class="seeWell cf"]//a[@class="clearfix stitle"]/@title').extract()
        book_url_list = response.xpath('//ul[@class="seeWell cf"]//a[@class="clearfix stitle"]/@href').extract()
        author_list = response.xpath('//ul[@class="seeWell cf"]//span/a[2]/text()').extract()
        category_list = response.xpath('//div[@class="main-index"]/a[2]/text()').extract()

        for title,author,category,book_link in zip(title_list,author_list,category_list,book_url_list):
            items = QuanshuwangSpiderItem()
            items['title'] = title
            items['author'] = author
            items['category'] = category
            items['book_link'] = book_link

            yield items

        next_url = response.xpath('//a[@class="next"]/@href').extract()

        if next_url:
            for i in next_url:
                yield scrapy.Request(i, callback=self.detail_parse)

