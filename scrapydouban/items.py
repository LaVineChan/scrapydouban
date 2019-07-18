# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydoubanItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	pass


class CommentItem(scrapy.Item):
	username = scrapy.Field()
	userlink = scrapy.Field()
	comment_time = scrapy.Field()
	useful_vote = scrapy.Field()
	comment = scrapy.Field()
	id = scrapy.Field()
	title = scrapy.Field()


# 定义电影item
class MovieItem(scrapy.Item):
	id = scrapy.Field()
	title = scrapy.Field()
	rating = scrapy.Field()
	alt = scrapy.Field()
