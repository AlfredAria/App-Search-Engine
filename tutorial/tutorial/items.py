# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
	desc = scrapy.Field()

class AppItem (scrapy.Item):
	title = scrapy.Field()
	appId = scrapy.Field()
	icon = scrapy.Field()
	introduction = scrapy.Field()
	url = scrapy.Field()
	recommended = scrapy.Field()

	# Image downloading
	image_urls = scrapy.Field() # A field to specify the image url
	images = scrapy.Field() # Will store information about the downloaded images