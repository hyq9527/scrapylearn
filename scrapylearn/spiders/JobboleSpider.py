# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from scrapylearn.items import JobboleArticleItem
from scrapylearn.utils.common import get_md5
import datetime
class JobbolespiderSpider(scrapy.Spider):
    name = 'JobboleSpider'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .post-thumb a")
        for post_node in post_nodes:
         post_url = post_node.css("::attr(href)").extract_first("")
         front_image_url = post_node.css("img::attr(src)").extract_first("")
         yield Request(url=parse.urljoin(response.url,post_url),
                       meta={"front_image_url":parse.urljoin(response.url, front_image_url)},
                       callback=self.parse_detail)
        #  next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self,response):
        try:
            title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
            create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()[1]').extract()[0].strip().replace("·","").strip();
            praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0].strip()
            fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
            match_re = re.match(".*?(\d+).*", fav_nums)
            if match_re:
               fav_nums = match_re.group(1)
            else:
                fav_nums = 0
            comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
            match_re = re.match(".*?(\d+).*", comment_nums)
            if match_re:
               comment_nums = match_re.group(1)
            else:
                comment_nums = 0
            content = response.xpath('//div[@class="entry"]').extract()[0]
            tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
            tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
            tags = ",".join(tag_list)
            front_image_url = response.meta.get("front_image_url", "")
            article_item = JobboleArticleItem()
            article_item["title"] = title
            try:
                create_date = datetime.datetime.strftime(create_date,"%Y/%m/%d").date()
            except Exception as e:
                create_date = datetime.datetime.now().date()

            article_item["create_date"] = create_date
            article_item["praise_nums"] = praise_nums
            article_item["fav_nums"] = fav_nums
            article_item["comment_nums"] = comment_nums
            article_item["content"] = content
            article_item["tags"] = tags
            article_item["front_image_url"] = [front_image_url]
            # article_item["front_image_path"] = front_image_path
            article_item["url"] = response.url
            article_item["url_object_id"] = get_md5(response.url)

            print(title)
            yield article_item
        except Exception as e:
            print("error-url=", response.url,e)