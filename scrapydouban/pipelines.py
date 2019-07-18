# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapydouban.items import MovieItem
import pandas as pd


class ScrapydoubanPipeline(object):
	def process_item(self, item, spider):
		# csv 写入
		# 打开文件，追加a
		out = open('.\comment.csv', 'a', newline='', encoding='gb18030')
		# 设定写入模式
		csv_write = csv.writer(out, dialect='excel')
		# 写入具体内容
		csv_write.writerow(
			[item["id"], item["title"], item["username"], item["comment_time"], item["comment"]])
		return item


# data = pd.read_csv(r'.\movie.csv',encoding='gbk')
# print(data.columns)  # 获取列索引值
# data['username'] = item["username"]
# data['userlink'] = item["userlink"]
# data['comment_time'] = item["comment_time"]
# data['useful_vote'] = item['useful_vote']
# data['comment'] = item['comment']
# data.to_csv(r".\movie.csv", mode='a', index=False)
# mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名


class MoviePipeline(object):
	def process_item(self, item, spider):
		movie = MovieItem()
		movie["id"] = item['id']
		movie["title"] = item['title']
		movie["rating"] = item['rating']
		movie["alt"] = item['alt']
		# csv 写入
		# 打开文件，追加a
		out = open('.\movie.csv', 'a', newline='')
		# 设定写入模式
		csv_write = csv.writer(out, dialect='excel')
		# 写入具体内容
		csv_write.writerow([movie["id"], movie["title"], movie["rating"], movie["alt"]])
		return item


class CommentPipeline(object):
	def process_item(self, item, spider):
		# csv 写入
		# 打开文件，追加a
		out = open('.\comment.csv', 'a', newline='')
		# 设定写入模式
		csv_write = csv.writer(out, dialect='excel')
		# 写入具体内容
		csv_write.writerow(
			[item["username"], item["userlink"], item["comment_time"], item["useful_vote"], item["comment"]])
		return item
