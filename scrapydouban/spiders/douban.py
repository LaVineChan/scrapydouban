# coding: utf-8
import scrapy
import requests
import json

import urllib
import csv
from scrapy.selector import Selector
from scrapydouban.items import CommentItem
from scrapydouban.items import MovieItem


class CommentSpider(scrapy.Spider):
	name = "comment"
	allow_domain = ['douban.com']
	custom_settings = {
		"ITEM_PIPELINES": {
			'scrapydouban.pipelines.ScrapydoubanPipeline': 300
		},
		"DOWNLOADER_MIDDLEWARES": {
			'scrapydouban.middlewares.UserAgentMiddleware': 401,
			'scrapydouban.middlewares.Cookies_Proxy_Middleware': 402,
		},
		"DEFAULT_REQUEST_HEADERS": {
			'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
		},
		"ROBOTSTXT_OBEY": False
	}

	# start_request
	def start_requests(self):
		loginin_url = "https://accounts.douban.com/passport/login?source=movie"
		# request1 = scrapy.Request(loginin_url, callback=self.parse_before_login)
		# 打开文件，读取文件
		out = open('.\movie.csv', 'r')
		reader = csv.reader(out)
		movieItems = []
		requests = []
		count = 0
		for line in reader:
			if count > 659:
				if line[0] != 'id':
					movieItem = MovieItem()
					movieItem['id'] = line[0]
					movieItem['title'] = line[1]
					movieItem['rating'] = line[2]
					movieItem['alt'] = line[3]
					movieItems.append(movieItem)
			count += 1

		out = open('.\comment.csv', 'a', newline='', encoding='gb18030')
		# 设定写入模式
		csv_write = csv.writer(out, dialect='excel')
		# 写入具体内容
		csv_write.writerow(["id", "title", "username", "comment_time", "comment"])
		for item in movieItems:
			id_url = '''https://movie.douban.com/subject/{commentid}/comments?status=P'''
			request = scrapy.Request(id_url.format(commentid=item["id"]), callback=self.dbSearch,
									 meta={'id': item["id"], 'title': item["title"]}, dont_filter=True)
			requests.append(request)
		return requests

	def dbSearch(self, response):
		id = response.request.meta['id']
		title = response.request.meta['title']
		selector = Selector(response)
		divs = selector.xpath('//div[@class="comment"]')
		for div in divs:
			commentItem = CommentItem()
			commentItem['useful_vote'] = div.xpath(
				'//span[@class="comment-vote"]/span[@class="votes"]/text()').extract()
			commentItem['username'] = div.xpath('//span[@class ="comment-info"]/a/text()').extract()
			commentItem['userlink'] = div.xpath('//span[@class ="comment-info"]/a/@href').extract()
			commentItem['comment_time'] = div.xpath(
				'//span[@class ="comment-info"]/span[@class="comment-time "]/@title').extract()
			commentItem['comment'] = div.xpath('//p[@class=""]//text()').extract()
			commentItem['id'] = id
			commentItem['title'] = title
		return commentItem

# def parse_before_login(self, response):
# 	print("登录前表单填充")
# 	captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
# 	captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
# 	if captcha_image_url is None:
# 		print(u"登录时无验证码")
# 		formdata = {
# 			"redir": "https://movie.douban.com/",
# 			"source": "movie",
# 			"form_email": "你的账号",
# 			# 请填写你的密码
# 			"form_password": "你的密码",
# 		}
# 		print(u"登录中")
# 		# 提交表单
# 		return scrapy.FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]},
# 												headers=self.headers, formdata=formdata,
# 												callback=self.parse_after_login)
# 	else:
# 		print("登录时有验证码")
# 		save_image_path = "D:/image/captcha.jpeg"
# 		# 将图片验证码下载到本地
# 		urllib.urlretrieve(captcha_image_url, save_image_path)
# 		# 打开图片，以便我们识别图中验证码
# 		try:
# 			im = Image.open('captcha.jpeg')
# 			im.show()
# 		except:
# 			pass
# 		# 手动输入验证码
# 		captcha_solution = raw_input('根据打开的图片输入验证码:')
# 		formdata = {
# 			"source": "None",
# 			"redir": "https://www.douban.com",
# 			"form_email": "你的账号",
# 			# 此处请填写密码
# 			"form_password": "你的密码",
# 			"captcha-solution": captcha_solution,
# 			"captcha-id": captcha_id,
# 			"login": "登录",
# 		}
#
# 	print("登录中")
# 	# 提交表单
# 	return scrapy.FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]},
# 											headers=self.headers, formdata=formdata,
# 											callback=self.parse_after_login)
