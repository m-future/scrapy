'''
Author: mfuture@qq.com
Date: 2021-10-13 17:03:51
LastEditTime: 2021-10-14 10:57:56
LastEditors: mfuture@qq.com
Description: 常用处理函数
FilePath: /health39/jbk39/lib/common.py
'''

import re

class strFunc():
    def cleanStr(string):
        #  表格中含有 \xa0 空格， \t tab制表符， \r \n 换行符，\u3000 中文全角空白符号
        string =re.sub(r'<[^>]+>', u"",string) # 替换标签,避免段落中有 <a> 标签
        string=string.replace(u'\u3000', u'').replace(u'\n', u'').replace(u'\r', u'').replace(u' ', u'').replace(u'\"', u'').replace(u'\t', u'').replace(u'\ax0',u'')
        
        return string
