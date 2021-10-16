'''
Author: mfuture@qq.com
Date: 2021-10-16 18:20:57
Description: 扫描代理IP更新其是否可用
FilePath: /health39/jbk39/lib/network.py
'''

import re
import time
import telnetlib
import gevent
from service import DatabaseService as db

# 检查网络状态


class NetCheck():

    def scan(self, proxy):
        try:
            server = telnetlib.Telnet()
            server.open(proxy['ip'], proxy['port'], 2)
            db.update_proxy(proxy,1)
        except Exception as e:
            db.update_proxy(proxy,0)
            pass

    def check_proxy(self):
        proxy_list = db.select_proxy()
        threads = [gevent.spawn(self.scan, proxy) for proxy in proxy_list]
        gevent.joinall(threads)


if __name__ == '__main__':
    NetCheck().check_proxy()
