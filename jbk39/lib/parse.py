'''
Author: mfuture@qq.com
Date: 2021-10-27 10:38:07
Description: 对爬取的数据进一步解析，获得想要的数据格式
'''


from scrapy import Selector
import re

# from common import StrFunc
from jbk39.lib.common import StrFunc


def clean_dic(children):
    if len(children)>0:
        for i,v in enumerate(children):
            del v['parent']
            del v['value']
            clean_dic(v['children'])




class FineParse():

    # 初始化
    def __init__(self):

        # self.regExp = r'[一二三四五六七八九十1-9](?![天个般是经～-])'
        self.regExp = r'[一二三四五六七八九十1-9]\d{0,}[\.、】\)）](?!\d)'
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
    def parse_item_treatment(self, response=None, path=None,title='治疗'):



        # string='11.2天去吧'

        # search=re.search(self.regExp,string)

        # print(search)

        # return

        result = {'title':title,'children': []}  # 存放解析后的结果

        paragraphs= response.xpath(path)

        # path = '//div[@class="article_paragraph"]/p'
        # paragraphs = self.local_selector().xpath(path)

        # 段落的类名
        paraClass = paragraphs.xpath('./@class').extract()

        # 段落的内容
        paraText = paragraphs.extract()
        paraText = list(map(lambda x: StrFunc().str_format(x), paraText))

        parent=None

        for i, content in enumerate(paraText):
            # print('==========================')
            # print(content)
            obj = None
            if paraClass[i] == 'article_title_num':
                obj = {'title': content, 'content': '',
                       'children': [], 'value': -1, 'parent': None}
                result['children'].append(obj)
                parent = obj
                continue

            search = re.search(self.regExp, content)

            # print(search)

            # 找到标题了
            if search and search.span()[0] < 2:

                value = self.parse_number(search.group(0))

                if paraClass[i] == 'article_name':  # 明确表明是标题
                    obj = {'title': content, 'content': '', 'children': []}
                else:  # 没有显式地标明是标题
                    obj = self.parse_content(self.regExp, content)

                obj['value'] = value

                # 如果等于之前标题序号加1，说明是同级标题，需要找到上级
                if value==1:
                    parent=parent
                elif value==parent['value']+1:
                    parent=parent['parent']
                else:
                    while parent['parent']:
                        parent = parent['parent']
                        if value == parent['value']+1:
                            parent=parent['parent']
                            break

                obj['parent'] = parent
                parent['children'].append(obj)
                parent = obj
            # 纯内容
            else:
                parent['content'] += content


        # print('-------------final result ---------------')



        clean_dic(result['children'])

        return result


    def parse_item_identify(self, response=None, path=None,title=''):
    

        result = {'title':'','children': []}  # 存放解析后的结果

        paragraphs= response.xpath(path)

        # 段落的类名
        paraClass = paragraphs.xpath('./@class').extract()

        # 段落的内容
        paraText = paragraphs.extract()
        paraText = list(map(lambda x: StrFunc().str_format(x), paraText))

        parent={'title': '', 'content': '',
                       'children': [], 'value': -1, 'parent': None}

        result['children'].append(parent)

        for i, content in enumerate(paraText):
            # print('==========================')
            # print(content)
            obj = None

            search = re.search(self.regExp, content)

            # print(search)

            # 找到标题了
            if search and search.span()[0] < 2:

                value = self.parse_number(search.group(0))

                if paraClass[i] == 'article_name':  # 明确表明是标题
                    obj = {'title': content, 'content': '', 'children': []}
                else:  # 没有显式地标明是标题
                    obj = self.parse_content(self.regExp, content)

                obj['value'] = value

                # 如果等于之前标题序号加1，说明是同级标题，需要找到上级
                if value==1:
                    parent=parent
                elif value==parent['value']+1:
                    parent=parent['parent']
                else:
                    while parent['parent']:
                        parent = parent['parent']
                        if value == parent['value']+1:
                            parent=parent['parent']
                            break

                obj['parent'] = parent
                parent['children'].append(obj)
                parent = obj
            # 纯内容
            else:
                if i==0:
                    parent['title'] += content
                else:
                    parent['content'] += content


        # print('-------------final result ---------------')


        clean_dic(result['children'])

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
            # title = content[span[0]:span[1]]
            result = {'title': content[span[0]:span[1]],
                      'content': content[span[1]:]}

        result['children'] = []

        return result


if __name__ == '__main__':
    FineParse().parse_item_treatment()
