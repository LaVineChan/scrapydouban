# scrapydouban
豆瓣影评爬虫
本个项目包括两个爬虫，一个movie爬虫，一个comment爬虫
1.movie爬虫
此爬虫是在豆瓣电影的网站上发现，通过利用Chrome的调试工具，在豆瓣电影-分类这个页面我发现了他们使用的一个JQuery接口,也是一个GET请求，不需要AUTH。https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=20，这个接口可以获取所有豆瓣上收录的电影，经过我的测试，start改为10000时，返回的数据就已经是空的了。所以通过不对返回的json数据，即获得了全部的电影基本信息。
2.comment爬虫
此爬虫思路源于每个电影的影评的url由电影的ID所决定，而电影id已经在第一个爬虫存入了，具体网址为https://movie.douban.com/subject/{commentid}/comments?status=P。影评的爬虫相比电影的爬虫更为困难，主要是爬取的数据较多，会触发豆瓣的反爬虫机制。
本项目采取以下行为应对发爬虫机制
（1）重构了UserAgentMiddleware和Cookies_Proxy_Middleware。其中UserAgentMiddlewar主要随机设置不同user-agent，Cookies_Proxy_Middleware为爬虫加上cookie，模拟登录。原来的DownloaderMiddleware也增加了安全ip名单
（2）尽可能多的模拟浏览器发送request请求所携带的参数
（3）设置DOWNLOAD_DELAY = 3
