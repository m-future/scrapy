'''
Author: mfuture@qq.com
Date: 2021-10-27 10:38:07
Description: 对爬取的数据进一步解析，获得想要的数据格式
'''


from scrapy import Selector
import re

# from common import StrFunc
from jbk39.lib.common import StrFunc


class FineParse():

    # 初始化
    def __init__(self):

        # self.regExp = r'[一二三四五六七八九十1-9](?![天个般是经～-])'
        self.regExp = r'[一二三四五六七八九十1-9]\d{0,}[\.、】\)）](?!\d)'
        # TODO: 考虑A-Z和①②③④⑤⑥⑦⑧⑨⑩编号
        self.regExp = r'[一二三四五六七八九十1-9]\d{0,}[\.、】\)）]'

    # 打开本地文件尽心解析

    def local_selector(self):
        fs = open('data/test.html')
        body = fs.read()
        selector = Selector(text=body)

        return selector

    # 解析治疗返回的数据
    # https://jbk.39.net/slgy/yyzl/ 输卵管炎
    # https://jbk.39.net/ydspnlyb/yyzl/ 阴道上皮内瘤样变
    def parse_item(self, response=None, path=None,title=''):

        result = []  # 存放解析后的结果

        paragraphs = response.xpath(path)

        # path = '//div[@class="article_paragraph"]/p'
        # paragraphs = self.local_selector().xpath(path)

        # 段落的类名
        paraClass = paragraphs.xpath('./@class').extract()

        # 段落的内容
        paraText = paragraphs.extract()
        paraText = list(map(lambda x: StrFunc().str_format(x), paraText))

        parent = {'title': '', 'content': ''}

        for i, content in enumerate(paraText):
            obj = {}
            search = re.search(self.regExp, content)
            if paraClass[i] in ('article_title_num','article_name'):
                obj = {'title': content, 'content': ''}
                parent = obj
                result.append(parent)
            # 找到标题了
            elif search and search.span()[0] < 2:

                if paraClass[i] == 'article_name':  # 明确表明是标题
                    obj = {'title': content, 'content': ''}
                elif len(paragraphs[i].xpath('./strong')) > 0:  # 用加黑表明
                    obj = {'title': content, 'content': ''}
                else:  # 没有显式地标明是标题
                    obj = self.parse_content(self.regExp, content)
                parent = obj
                result.append(parent)

            else:
                if len(parent['content']) == 0:
                    parent['content'] = content
                else:
                    parent['content'] += '\\r\\n' + \
                        content if len(content) > 0 else ''

        if len(paraText)==1:
            parent['title']=title
            result.append(parent)

        # print('-------------final result ---------------')

        # print(result)

        delete_count = 0
        for i in range(len(result)):
            if len(result[i-delete_count]['content']) == 0:
                del(result[i-delete_count])
                delete_count += 1

        return result

    # 解析出数字

    def parse_number(self, content):
        hanji_to_number = {
            '一': 1,
            '二': 2,
            '三': 3,
            '四': 4,
            '五': 5,
            '六': 6,
            '七': 7,
            '八': 8,
            '九': 9,
            '十': 10,
            '十一': 11,
            '十二': 12,
        }
        regExp = r'[一二三四五六七八九十\d]+'
        search = re.search(regExp, content)

        match = search.group(0)

        try:
            return int(match)
        except Exception:
            return hanji_to_number[match]

    # 解析段落内容 根据1.2.这种标志
    def parse_content(self, regepx, content):
        result = {}
        span = re.search(regepx, content).span()
        title = re.search(r'[：:]', content)
        if title:
            titlePosi = title.span()[1]
            title = content[:titlePosi]
            # title = re.sub(regepx, u'', title)
            content = content[titlePosi:]
            result = {'title': title, 'content': content}
        else:
            result = {'title': content[span[0]:span[1]],
                      'content': content[span[1]:]}

        return result


if __name__ == '__main__':
    FineParse().parse_item()
