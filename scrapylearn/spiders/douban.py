# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/']
    header = {
        "Host":"www.douban.com",
        "Origin": "https://www.douban.com",
        "Referer":"https://www.douban.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request("https://www.douban.com/",headers=self.header,callback=self.login)]

    def login(self,response):
        return [scrapy.FormRequest(
            url="https://www.douban.com/accounts/login",
            formdata={
                "source":"index_nav",
                "form_email":"527446203@qq.com",
                "form_password":"hyq19900625"
            },
            headers=self.header,
            callback=self.check_login,
            dont_filter=True
        )]

    def check_login(self,response):
        if "https://www.douban.com/mine/" in response.text:
            for url in self.start_urls:
                yield scrapy.Request(url=url,headers=self.header,dont_filter=True)
        pass
