'''
Author: mfuture@qq.com
Date: 2021-04-22 14:35:56
Description: 
FilePath: /health39/jbk39/settings.py
'''

import datetime
# Scrapy settings for jbk39 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# or from local file:
# /Library/Python/3.8/site-packages/scrapy/settings/default_settings.py


BOT_NAME = 'jbk39'

SPIDER_MODULES = ['jbk39.spiders']
NEWSPIDER_MODULE = 'jbk39.spiders'

ITEM_PIPELINES = {
    'jbk39.pipelines.Jbk39Pipeline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jbk39 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 日志记录
LOG_LEVEL = 'INFO'  # 由高到低等级分为：CRITICAL ERROR WARNING INFO DEBUG
to_day = datetime.datetime.now()
# 注意此处相对路径的写法，必须带上项目名称目录
log_file_path = './jbk39/log/scrapy_{}_{}_{}.log'.format(
    to_day.year, to_day.month, to_day.day)
LOG_FILE = log_file_path

# 超时
DOWNLOAD_TIMEOUT = 5

# NOTE:是否使用 ip 代理
USE_IP_PROXY = True

# 保存爬虫中断（ctrl+z）时的数据，以便恢复-fg, 查看进程-jobs
# 最好在每个爬虫那里自己设置
JOBDIR='./jobs/'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 如果有多个spider情况下，一共允许的并发请求
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# 随机化delay= (0.5~1.5) * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16

'''
对单个IP进行并发请求的最大值。如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定，
使用该设定。 也就是说，并发限制将针对IP，而不是网站。
该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0，
下载延迟应用在本地IP而不是远程网站上。
也就是说 网站会每隔 DOWNLOAD_DELAY 时间收到 爬虫产生的 并发。
'''

CONCURRENT_REQUESTS_PER_IP = 16

# 重试次数，默认为 2 次，即对一地址会请求 initial + retry = 3 次
RETRY_TIMES = 2

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'jbk39.middlewares.Jbk39SpiderMiddleware': 544,  # 执行顺序
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'jbk39.middlewares.Jbk39DownloaderMiddleware': 543,
    'jbk39.middlewares.RandomUserAgent': 542,
    'jbk39.middlewares.ProcessAllExceptionMiddleware': 50,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'jbk39.pipelines.Jbk39Pipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
