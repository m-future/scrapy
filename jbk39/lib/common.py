'''
Author: mfuture@qq.com
Date: 2021-10-13 17:03:51
LastEditTime: 2021-10-13 20:17:38
LastEditors: mfuture@qq.com
Description: 常用处理函数
FilePath: /health39/jbk39/lib/common.py
'''

import re

class strFunc():
    def cleanStr(string):
        string =re.sub(r'<[^>]+>', u"",string) # 替换标签,避免段落中有 <a> 标签
        string=string.replace(u'\u3000', u'').replace(u'\n', u'').replace(u'\r', u'').replace(u' ', u'').replace(u'\"', u'')
        
        return string
