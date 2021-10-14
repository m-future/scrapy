'''
Author: mfuture@qq.com
Date: 2021-04-21 16:41:24
LastEditTime: 2021-10-14 22:57:23
LastEditors: mfuture@qq.com
Description: scrapy middleware
FilePath: /health39/jbk39/middlewares.py
'''
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware 
from fake_useragent import UserAgent # 生成随机 useragent  

from scrapy.http import HtmlResponse
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet import defer
from twisted.web.client import ResponseFailed

from jbk39.lib.db_service import database as db

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

# 随机选择一个 代理
def random_proxy(proxy=None):
    res=db.random_proxy(proxy)
    proxy="http://{}:{}".format(res['ip'],res['port'])
    return proxy
    




class Jbk39DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)    

    
    def __init__(self):
        self.proxy=random_proxy()

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

        # self.proxy= "http://113.96.219.105:4015"

        request.meta['proxy'] = self.proxy
      
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        
        # 一定要搞清楚路径，你在第一层根目录下
        fs=open('data/HtmlResponse.html','w')
        fs.write(response.body.decode())
        fs.close()
        
        return response

    def process_exception(self, request, exception, spider):


        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            print(exception)
            spider.logger.info("[Got exception]   {}".format(exception))
            spider.logger.info("[需要更换代理重试，之前代理为]   {}".format('self.proxy'))
            
            self.proxy=random_proxy(self.proxy)

            new_request = request.copy()
            new_request_l = new_request.replace(url=request.url)
            return new_request_l
        # 打印出未捕获到的异常
        spider.logger.info("[not contained exception]   {}".format(exception))

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(UserAgentMiddleware):    # 如何运行此中间件? settings 直接添加就OK
    def process_request(self, request, spider):
        # ua = random.choice(user_agent_list)
        # 关于可能出现的错误请参考这篇文档 https://blog.csdn.net/yilovexing/article/details/89044980
        ua = UserAgent().random
        # 在请求头里设置ua
        request.headers.setdefault("User-Agent",ua)