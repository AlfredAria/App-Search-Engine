# app_spider.py

# Alfred Huang
# Dec 20, 2015

# References:
# Scrapy tutorial: http://doc.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments
# UTF-8: http://stackoverflow.com/questions/5203105/printing-a-utf-8-encoded-string

# Convenient nodes:
# 

import scrapy
import re

from tutorial.items import AppItem;

class AppSpider(scrapy.Spider):
    name = "app"
    allowed_domains = ["huawei.com"]
    start_urls = [
        "http://appstore.huawei.com"
    ]

    # Sadly reference here: http://blog.siliconstraits.vn/building-web-crawler-scrapy/
    # manually records all crawled pages, otherwise there are duplications... 
    crawled_ones = []

    def parse(self, response):
        # Retrieve all urls from the webpage
        for href in response.xpath("//a/@href"):
            link = href.extract()
            # Exclude pages that does not satisfy the app url pattern
            if re.match ("http://appstore.huawei.com:80/app/.*", href.extract()) is None:
                continue
            # If necessary convert a relative link into an absolute one

            # Avoid re-crawling
            if link in self.crawled_ones: 
                continue
            self.crawled_ones += link

            url = response.urljoin(link)
            # Trick to pass parameter to the callback:
            # Put KV pairs in the meta field
            request = scrapy.Request(url, callback=self.parse_dir_contents)
            request.meta["appId"] = url[url.rfind('/') + 1:] # Obtain the appId

            # Create a generator for upcoming urls to scrape pages
            yield request

    # Collect response information into Items
    def parse_dir_contents(self, response):

        # Why aggregate multiple ones?
        for sel in response.xpath('//ul/li'):
            item = AppItem()
            # I found multiple 'title' fields with this selector. Any better one?
            item['title'] = sel.xpath('//span[@class="title"]/text()').extract()[0]
            # App id is exactly the filename in the url
            item['appId'] = response.meta["appId"]
            # Get app_default when retrieving.
            # How to solve this?
            item['icon'] = sel.xpath('//img[@class="app-ico"]/@src').extract()
            #
            item['introduction'] = sel.xpath('//div[@id="app_strdesc"]/text()').extract()
            yield item
            break


    # def set_crawler(self, crawler):
    #     super(AppSpider, self).set_crawler(crawler)
    #     crawler.settings.set('DEPTH_LIMIT','10')

# Note: One way to read and check utf-8 output:
# print response.xpath('//div[@id="app_strdesc"]/text()').extract()[0].encode('utf-8')


