# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests
import json
import scrapy
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class UserAgentMiddleware(object):
	""" 换User-Agent """

	def process_request(self, request, spider):
		agents = [
			"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
			"Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
			"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
			"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre", ]

		agent = random.choice(agents)
		request.headers["User-Agent"] = agent


'''
class ProxyMiddleware(object):


    def process_request(self,request,spider):
        """ 为爬虫加上代理IP，避免IP被封"""
        proxyres = requests.get('http://proxy.nghuyong.top').text
        totalproxies = json.loads(proxyres)['num']
        if (totalproxies>0):
            proxylist=json.loads(proxyres)['data']
            proxy = random.choice(proxylist)
            request.meta['proxy'] ="http://"+proxy['ip_and_port']
'''


class Cookies_Proxy_Middleware(RetryMiddleware):
	""" 维护Cookie 和代理IP"""

	def __init__(self, settings, crawler):
		RetryMiddleware.__init__(self, settings)

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings, crawler)

	def process_request(self, request, spider):
		""" 为爬虫加上cookie，模拟登录 """
		mycookie = '_vwo_uuid_v2=B6EE2F2ABC6F6FC9B7065267E734D090|4ad5e1d9e56a27b26ce66957cc5b09be; gr_user_id=8dc68eaa-8b72-43f4-84a6-6c0f650c7c3a; douban-fav-remind=1; __utmv=30149280.13920; ll="118267"; bid=pn69xRuKcjM; __utma=30149280.415852480.1530538687.1547949882.1551433873.8; __utmz=30149280.1551433873.8.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1551433887%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DD5rNRCuc2rv2CHn1ckC5aKqKaJBXBOddlSbX_G4iGwj6WsxXDEpAiXZsiKh6ZuXK%26wd%3D%26eqid%3Dec93ffb6000138d0000000065c790098%22%5D; __utma=223695111.1744664372.1538477885.1547949897.1551433887.3; __utmz=223695111.1551433887.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.4cf6=80729bfb43502673.1514548904.7.1551434239.1547951154.; viewed="5976569"; push_noty_num=0; push_doumail_num=0; ap_v=0,6.0'
		request.cookies = self.builddict(mycookie)

	''' 因为request接受的cookie是字典形式，所以要把从浏览器赋值过来的cookie解析成字典形式 '''

	def builddict(self, string):
		cookiedic = {}
		dictstr = '{'
		linelist = string.split(';')
		for line in linelist:
			key = line.split('=')[0]
			value = line.split('=')[1]
			dictstr = dictstr + '"' + key + '"' + ':' + "'" + value + "'" + ','
			cookiedic[key] = value
		dictstr = dictstr.rstrip(',')
		dictstr = dictstr + '}'
		# print(dictstr)
		return cookiedic

	def process_response(self, request, response, spider):
		if response.status in [403, 414]:
			reason = response_status_message(response.status)
			print('change ip proxy and retrying...')
			proxyres = requests.get('http://proxy.nghuyong.top').text
			totalproxies = json.loads(proxyres)['num']
			if (totalproxies > 0):
				proxylist = json.loads(proxyres)['data']
				proxy = random.choice(proxylist)
				request.meta['proxy'] = "http://" + proxy['ip_and_port']
				return self._retry(request, reason, spider)
		# print("%s! Stopping..." % response.status)
		# os.system("pause")
		else:
			return response


class ScrapydoubanDownloaderMiddleware(object):
	ip_list = None

	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the downloader middleware does not modify the
	# passed objects.
	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		# Called for each request that goes through the downloader
		# middleware.

		# Must either:
		# - return None: continue processing this request
		# - or return a Response object
		# - or return a Request object
		# - or raise IgnoreRequest: process_exception() methods of
		#   installed downloader middleware will be called
		if self.ip_list is None or len(self.ip_list) == 0:
			response = requests.request('get',
										'http://api3.xiguadaili.com/ip/?tid=555688914990728&num=10&protocol=https').text
			self.ip_list = response.split('\r\n')

		ip = random.choice(self.ip_list)
		request.meta['proxy'] = "https://" + ip
		print("当前proxy:%s" % ip)
		self.ip_list.remove(ip)
		return None

	def process_response(self, request, response, spider):
		def process_response(self, request, response, spider):
			# Called with the response returned from the downloader.
			# Must either;
			# - return a Response object
			# - return a Request object
			# # - or raise IgnoreRequest

			return response

	def process_exception(self, request, exception, spider):
		# Called when a download handler or a process_request()
		# (from other downloader middleware) raises an exception.

		# Must either:
		# - return None: continue processing this exception
		# - return a Response object: stops process_exception() chain
		# - return a Request object: stops process_exception() chain
		pass

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)
