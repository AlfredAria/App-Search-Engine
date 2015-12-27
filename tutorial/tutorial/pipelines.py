# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class TutorialPipeline(object):
	def __init__ (self):
		self.file = open ("appstore.dat", "wb")

	def process_item(self, item, spider):
		val = "{0}\t{1}\t{2}\t{3}\n".encode("UTF-8").format(item['appId'], item['title'], item['icon'], item['introduction'])
		self.file.write(val)
		return item

class AppIconPipeline(ImagesPipeline):

	# Reference on customizing image file naming
	# http://stackoverflow.com/questions/6194041/scrapy-image-download-how-to-use-custom-filename

	# (Deprecated) Name download version
	# def image_key(self, url):
	# 	image_guid = url.split('/')[-1]
	# 	return 'full/%s.jpg' % (image_guid)

	# # (Deprecated) Name thumbnail version
	# def thumb_key(self, url, thumb_id):
	# 	image_guid = thumb_id + url.split('/')[-1]
	# 	return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

	# Useful
	def file_path(self, request, response=None, info=None):
		print request.url
		image_guid = request.url.split('/')[-1]
		return 'full/%s' % (image_guid)

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no files")
		return item