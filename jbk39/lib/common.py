'''
Author: mfuture@qq.com
Date: 2021-10-13 17:03:51
LastEditTime: 2021-10-14 17:36:52
LastEditors: mfuture@qq.com
Description: 常用处理函数
FilePath: /health39/jbk39/lib/common.py
'''

import re
import time

class strFunc():
    # 清除中英混合的空格
    def clean_space(self,text):
        match_regex = re.compile(u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
        should_replace_list = match_regex.findall(text)
        order_replace_list = sorted(should_replace_list,key=lambda i:len(i),reverse=True)
        for i in order_replace_list:
            if i == u' ':
                continue
            new_i = i.strip()
            text = text.replace(i,new_i)
        return text

    def cleanStr(self,string):
        # FIXME: 字符串中还有表示小于号 < 的&lt;和 表示大于号 > 的&gt; 等 html标签，是否替换有待商榷
        #  表格中含有 \xa0 空格， \t tab制表符， \r \n 换行符，\u3000 中文全角空白符号
        string =re.sub(r'<[^>]+>', u'',string) # 替换标签,避免段落中有 <a> 标签
        string=string.replace(u'\'',u'&apos;').replace(u'\"',u'&quot;').replace(u'\\',u'/') # html转义便于存储
        string=string.replace(u'\u3000', u'').replace(u'\n', u'').replace(u'\r', u'').replace(u'\t', u'').replace(u'\xa0',u'')
        string=self.clean_space(string) # 去除多余的空格
        return string
