# -*- coding: utf-8 -*-
import io
import sys
import csv
import requests

# 屏蔽warning信息
requests.packages.urllib3.disable_warnings()
url = 'https://www.douban.com/accounts/login'
html = requests.get(url, verify=False).text
with open('.\moviechoose1.txt', 'w', encoding='utf-8') as f:
	f.write(html)

# out = open('.\spiders\movie.csv', 'r')
# reader = csv.reader(out)
# ids = []
# count = 0
# for line in reader:
#         ids.append(line[0])
# print(ids)
