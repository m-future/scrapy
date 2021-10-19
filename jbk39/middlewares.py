'''
Author: mfuture@qq.com
Date: 2021-04-21 16:41:24
Description: scrapy middleware
FilePath: /health39/jbk39/middlewares.py
'''
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy import signals


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


import time
import json
import random
import shutil
import os


from jbk39.lib.service import DatabaseService as db


class Jbk39SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Jbk39DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        pass

    @classmethod
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        # 一定要搞清楚路径，你在第一层根目录下
        if spider.settings.get("WRITE_HTML_RESPONSE"):
            fs = open('data/htmlResponse.html', 'w')
            fs.write(response.body.decode())
            fs.close()

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

        return None



# 处理异常中间件，order=50 ，作为兜底的中间件

class ProcessAllExceptionMiddleware(object):

    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def __init__(self, spider):
        with open('jbk39/lib/config/fake_useragent.json','r') as f:
            self.agent = json.load(f)['browsers']['chrome']
            self.ua = random.choice(self.agent)

        # print(spider.spider.name) # 爬虫名字
        # 删除之前的jobs，否则spider认为已经完成工作，会立即停止

        job_dir=spider.settings.get('JOBDIR')
        shutil.rmtree(job_dir)

        # 是否开启代理
        self.useProxy = spider.settings.get("USE_IP_PROXY")

        # 避免连续更换代理
        self.last_change_proxy_time = time.time()

        if self.useProxy:
            self.proxy = db.select_random_proxy()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # crawler 就是 spider
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 好像爬取ip代理网站时不能用代理（更严格的反爬措施，或者仅仅是因为ip在他们的池子里）

        request.headers.setdefault("User-Agent", self.ua)

        if self.useProxy:
            request.meta['proxy'] = self.proxy
        return None

    def process_response(self, request, response, spider):
        # 有响应，但响应内容错误
        # 捕获状态码为40x/50x的response
        # FIXME: 还有可能 使用一些伪造的 response 数据

        bodyLen = len(response.body.decode())

        if int(response.status) != 200 or bodyLen < 500:
            spider.logger.warning(
                "[BAD RESPONSE], url: {}".format(request.url))
            if int(response.status) != 200:
                spider.logger.info(
                    "[BAD RESPONSE], statusCode: {}".format(response.status))
            if bodyLen < 500:
                spider.logger.info(
                    "[BAD RESPONSE], response: {}".format(response.body.decode()))
            self.proxy = self.change_proxy(spider, request)

            new_request = request.copy()
            new_request.dont_filter = True
            # new_request_l = new_request.replace(url=request.url)
            return new_request

        return response

    def process_exception(self, request, exception, spider):
        # 没有响应，则跳转到这里
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            spider.logger.warning("[Got exception with proxy: {}]   {}".format(
                request.meta['proxy'], exception))
            self.proxy = self.change_proxy(spider, request)
            # 继续请求
            new_request = request.copy()
            new_request.dont_filter = True
            # new_request_l = new_request.replace(url=request.url)
            return new_request
            # return request

        # 打印出未捕获到的异常
        spider.logger.warning(
            "[not contained exception]   {}".format(exception))

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    # 更换代理 ip
    def change_proxy(self, spider, request):

        if not self.useProxy:
            return

        currentProxy = self.proxy  # 更换以后的代理
        requestProxy = request.meta['proxy']  # 这个异常request的代理， 有可能使用的是更换之前的代理

        if requestProxy == currentProxy and time.time()-self.last_change_proxy_time > 5:
            # 如果不等于，说明该request 使用的是之前的代理，所以不需要更换，只需要用当前的代理重新请求一次就可以
            self.last_change_proxy_time = time.time()
            newProxy = db.select_random_proxy(currentProxy)
            self.ua = random.choice(self.agent) # 更换 useragent
            spider.logger.info(
                "[更换代理重试]   {} => {}".format(currentProxy, newProxy))
            print('更换代理： {} => {}'.format(currentProxy, newProxy))
            return newProxy
        time.sleep(0.5)
        return currentProxy
