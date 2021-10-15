'''
Author: mfuture@qq.com
Date: 2021-04-21 16:41:24
LastEditTime: 2021-10-15 15:53:18
LastEditors: mfuture@qq.com
Description: scrapy middleware
FilePath: /health39/jbk39/middlewares.py
'''
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.web.client import ResponseFailed
from scrapy.http import HtmlResponse
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.internet import defer
from scrapy import signals
import random
import logging
import time
import sys

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent  # 生成随机 useragent


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
    # FIXME: 如果proxy本身就是nonetype
    ipproxy = db.random_proxy(proxy)

    if not ipproxy:
        raise ValueError("ipproxy should not be %s " % (type(ipproxy)))
        # sys.exit(1)
    proxy = "http://{}:{}".format(ipproxy['ip'], ipproxy['port'])
    return proxy


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
        fs = open('data/HtmlResponse.html', 'w')
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




class RandomUserAgent(UserAgentMiddleware):    # 如何运行此中间件? settings 直接添加就OK
    def process_request(self, request, spider):
        # ua = random.choice(user_agent_list)
        # 关于可能出现的错误请参考这篇文档 https://blog.csdn.net/yilovexing/article/details/89044980
        ua = UserAgent().random
        # 在请求头里设置ua
        request.headers.setdefault("User-Agent", ua)


'''
处理异常中间件，order=50 ，作为兜底的中间件
'''


class ProcessAllExceptionMiddleware(object):

    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def __init__(self):
        self.proxy = random_proxy()

    @classmethod 
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 好像爬取ip代理网站时不能用代理（更严格的反爬措施，或者仅仅是因为ip在他们的池子里）
        request.meta['proxy'] = self.proxy
        return None


    def process_response(self, request, response, spider):
        # 有响应，但响应内容错误
        # 捕获状态码为40x/50x的response
        # FIXME: 还有可能 使用一些伪造的 response 数据

        bodyLen=len(response.body.decode())

        if int(response.status) != 200 or bodyLen < 500:
            spider.logger.warning("[BAD RESPONSE], statusCode: {}".format(response.status))
            spider.logger.warning("[BAD RESPONSE], response: {}".format(response.body.decode()))
            spider.logger.info("[需要更换代理重试，之前的代理为]   {}".format(self.proxy))     
            self.proxy = random_proxy(self.proxy)
            spider.logger.info("[更换之后的代理为]   {}".format(self.proxy))

            return request
            
        return response

    def process_exception(self, request, exception, spider):
        # 没有响应，则跳转到这里
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            spider.logger.warning("[Got exception]   {}".format(exception))
            spider.logger.info("[需要更换代理重试，之前的代理为]   {}".format(self.proxy))
            self.proxy = random_proxy(self.proxy)
            spider.logger.info("[更换之后的代理为]   {}".format(self.proxy))
            # response = HtmlResponse(url='exception')
            print("[exc 更换之后的代理为]   {}".format(self.proxy))
            # 继续请求
            return request

        # 打印出未捕获到的异常
        spider.logger.warning(
            "[not contained exception]   {}".format(exception))

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def change_proxy(self):
        pass
