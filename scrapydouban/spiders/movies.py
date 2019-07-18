# coding: utf-8
import scrapy
import requests
import json
import csv

from scrapydouban.items import MovieItem


class MovieSpider(scrapy.Spider):
	name = 'movie'  # 爬虫名称
	allow_dominas = ["douban.com"]  # 允许的域名

	# 自定义的爬虫设置，会覆盖全局setting中的设置
	custom_settings = {
		"ITEM_PIPELINES": {
			'scrapydouban.pipelines.MoviePipeline': 300
		},
		"DEFAULT_REQUEST_HEADERS": {
			'accept': 'application/json, text/javascript, */*; q=0.01',
			'accept-encoding': 'gzip, deflate',
			'Cookie': '_vwo_uuid_v2=B6EE2F2ABC6F6FC9B7065267E734D090|4ad5e1d9e56a27b26ce66957cc5b09be; gr_user_id=8dc68eaa-8b72-43f4-84a6-6c0f650c7c3a; douban-fav-remind=1; __utmv=30149280.13920; ll="118267"; bid=pn69xRuKcjM; __utma=30149280.415852480.1530538687.1547949882.1551433873.8; __utmz=30149280.1551433873.8.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1551433887%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DD5rNRCuc2rv2CHn1ckC5aKqKaJBXBOddlSbX_G4iGwj6WsxXDEpAiXZsiKh6ZuXK%26wd%3D%26eqid%3Dec93ffb6000138d0000000065c790098%22%5D; __utma=223695111.1744664372.1538477885.1547949897.1551433887.3; __utmz=223695111.1551433887.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.4cf6=80729bfb43502673.1514548904.7.1551434239.1547951154.; viewed="5976569"; ap_v=0,6.0',
			'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
			'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.KDdsmP',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
			'x-requested-with': 'XMLHttpRequest',
		},
		"ROBOTSTXT_OBEY": False  # 需要忽略ROBOTS.TXT文件
	}

	def start_requests(self):
		url = '''https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={start}'''
		requests = []
		# csv 写入
		# 打开文件，追加a
		out = open('.\movie.csv', 'a', newline='')
		# 设定写入模式
		csv_write = csv.writer(out, dialect='excel')
		# 写入具体内容
		csv_write.writerow(["id", "title", "rating", "alt"])
		for i in range(100):
			request = scrapy.Request(url.format(start=i * 20), callback=self.parse_movie)
			requests.append(request)
		return requests

	def parse_movie(self, response):
		jsonBody = json.loads(response.body)
		subjects = jsonBody['data']
		movieItems = []
		for subject in subjects:
			item = MovieItem()
			item['id'] = int(subject['id'])
			item['title'] = subject['title']
			item['rating'] = float(subject['rate'])
			item['alt'] = subject['url']
			movieItems.append(item)
		return movieItems
