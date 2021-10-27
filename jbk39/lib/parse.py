'''
Author: mfuture@qq.com
Date: 2021-10-27 10:38:07
Description: 对爬取的数据进一步解析，获得想要的数据格式
'''


from scrapy import Selector
import re

from common import StrFunc


class FineParse():

    # 初始化
    def __init__(self):

        self.treatment_level = [
            r'(中西医分类)',
            r'[一二三四五六七八九十][\.\、]',
            r'（[一二三四五六七八九十]）',
            r'(（\d）)|(\(\d\))|(\d[\.、])',
        ]

    # 打开本地文件尽心解析

    def local_selector(self):
        fs = open('data/test.html')
        body = fs.read()
        selector = Selector(text=body)

        return selector

    # 解析治疗返回的数据
    # https://jbk.39.net/slgy/yyzl/ 输卵管炎
    # https://jbk.39.net/ydspnlyb/yyzl/ 阴道上皮内瘤样变
    def parse_item_treatment(self, response=None, path=None):

        result = {"children":[]}  # 存放解析后的结果

        parent_level_index={0:'init',1:'init',2:'init',3:'init'} # 上层标题

        # paragraphs= response.xpath(path)

        path = '//div[@class="article_paragraph"]/p'
        paragraphs = self.local_selector().xpath(path)

        # 段落的类名
        paraClass = paragraphs.xpath('./@class').extract()

        # 段落的内容
        paraText = paragraphs.extract()
        paraText = list(map(lambda x: StrFunc().str_format(x), paraText))

        level=0 # 层级
        child=None

        for i, content in enumerate(paraText):
            print('========================')
            print(content)
            obj=None
            if paraClass[i] == 'article_title_num':
                obj = {'title': content, 'content': '', 'children': [], 'level': 0}
                level=0
                child=obj
                parent_level_index={0:parent_level_index[0],1:'init',2:'init',3:'init'} # 上层标题
                parent_level_index[0]=0 if parent_level_index[0]=='init' else parent_level_index[0]+1
            for j, regepx in enumerate(self.treatment_level):
                search = re.search(regepx, content)
                if search and search.span()[0] < 3:  # 过滤文本中的一些数字比如 0.4克，1、2贴每天
                    print(re.search(regepx, content))
                    parent_level_index[j]=0 if parent_level_index[j]=='init' else parent_level_index[j]+1
                    level=j
                    if paraClass[i]=='article_name': # 明确表明是标题
                        obj = {'title': content, 'content': '', 'children': [], 'level': level}
                        child=obj
                    else: # 没有显式地标明是标题
                        obj=self.parse_content(regepx,content)
                        obj['children']=[]
                        obj['level']=level
                        child=obj
                    break

            else: # 没有解析到标题，则整个段落作为内容
                print('meizhodao---')

            parent=result

            print('level:{}'.format(level))
            for i in range(level):
                try:
                    parent=parent['children'][parent_level_index[i]]
                except Exception:
                    parent=parent
                

            if not obj:
                print('----obj------')
                child['content']=content
            else:
                parent['children'].append(obj)


            print('+++++++++++++++++++++++++++++++')



        print('-------------final result ---------------')

        print(result)

        # test_text='一、'
        # rerext=r'(（\d）)|(\d[\.、])'
        # rerext=r'[一二三四五六七八九十][\.\、]'
        # search= re.search(rerext,test_text)

        # print('search: {}'.format(search))

        # indexes=[i for i, x in enumerate(lists) if x=='article_title_num']

        # print(len(lists),indexes)

        # indexes.append(len(lists))

        return

        for i, x in enumerate(indexes):
            if i == len(indexes)-1:
                break

            title = paragraphs[x].extract()

            content = self.parse_paragraph_l4(
                paragraphs[x+1:indexes[i+1]].extract())

            title = StrFunc().str_format(title)

            title = re.sub(r'[：:]', u'', title)
            title = re.sub(r'.*）', u'', title)
            title = re.sub(r'.*\d\.', u'', title)

            if len(content) > 0:
                if isinstance(content, list):
                    for x in content:
                        results.append(x)
                else:
                    results.append({'title': title, 'content': content})

        # 没有 class ='article_name' , 标题和内容混合在一起了
        if len(indexes) == 1:
            content = self.parse_paragraph_l3(paragraphs.extract())

            for x in content:
                results.append(x)

        return results

    # 解析段落内容 根据1.2.这种标志
    def parse_content(self, regepx,content):
        result = {}
        span=re.search(regepx, content).span()
        title = re.search(r'[：:]', content)
        if  title:
            titlePosi = title.span()[1]
            title = content[:titlePosi-1]
            title = re.sub(regepx, u'', title)
            content = content[titlePosi:]
            result={'title': title, 'content': content}
        else:
            title=content[span[0]:span[1]] # 
            result={'title': content[span[0]:span[1]], 'content': content[span[1]:]}
        return result



    def parse_paragraph(self, paragraphs, className):

        results = []
        lists = paragraphs.xpath('./@class').extract()

        indexes = [i for i, x in enumerate(lists) if x == 'article_name']

        indexes.append(len(lists))

        for i, x in enumerate(indexes):
            if i == len(indexes)-1:
                break

            title = paragraphs[x].extract()

            content = self.parse_paragraph_l2(
                paragraphs[x+1:indexes[i+1]].extract())

            title = StrFunc().str_format(title)

            title = re.sub(r'[：:]', u'', title)
            title = re.sub(r'.*）', u'', title)
            title = re.sub(r'.*\d\.', u'', title)

            if len(content) > 0:
                if isinstance(content, list):
                    for x in content:
                        results.append(x)
                else:
                    results.append({'title': title, 'content': content})

        # 没有 class ='article_name' , 标题和内容混合在一起了
        if len(indexes) == 1:
            content = self.parse_paragraph_l3(paragraphs.extract())

            for x in content:
                results.append(x)

        return results

        # 解析段落 根据1.2.这种标志
    def parse_paragraph_l2(self, paras):
        results = []
        sub_title_found = False

        paras = list(map(lambda x: StrFunc().str_format(x), paras))

        for x in paras:
            label = re.search(r'\d\.', x)
            title = re.search(r'[：:]', x)

            if label and title:
                sub_title_found = True
                titlePosi = title.span()[1]
                title = x[:titlePosi-1]
                title = re.sub(r'.*）', u'', title)
                title = re.sub(r'.*\d\.', u'', title)

                content = x[titlePosi:]
                results.append({'title': title, 'content': content})
            else:
                results.append({'title': None, 'content': x})

        if not sub_title_found:

            results = ''.join(paras)

        return results


# 卵巢成熟畸胎瘤 外阴乳头状瘤 女性生殖道多部位原发癌

        # 解析段落 根据1.2.这种标志

    def parse_paragraph_l3(self, paras):

        results = []

        paras = list(map(lambda x: StrFunc().str_format(x), paras))

        purecontent = ''.join(paras)

        paras = '#'.join(paras)

        index_list = [i.start() for i in re.finditer(r'\d[\.、]', paras)]

        # index_list = [i.start() for i in re.finditer('(\d、)|(\d\.)', paras)]

        index_list.append(len(paras))

        title_found = False

        for i, x in enumerate(index_list):

            if i == len(index_list)-1:
                break

            title_found = True

            ok = paras[x:index_list[i+1]]

            title = ok.split('#')[0]

            title = re.sub(r'(\d[\.、])|[:：]', '', title)
            content = ''.join(ok.split('#')[1:])
            results.append({'title': title, 'content': content})

        if not title_found:
            results.append({'title': None, 'content': purecontent})
        return results

    # 解析段落 根据一、二、这种标志
    def parse_paragraph_l4(self, paras):

        results = []

        paras = list(map(lambda x: StrFunc().str_format(x), paras))

        purecontent = ''.join(paras)

        paras = '#'.join(paras)

        index_list = [i.start()
                      for i in re.finditer(r'[一二三四五六七八九十][、\.]', paras)]

        # index_list = [i.start() for i in re.finditer('(\d、)|(\d\.)', paras)]

        index_list.append(len(paras))

        title_found = False

        for i, x in enumerate(index_list):

            if i == len(index_list)-1:
                break

            title_found = True

            ok = paras[x:index_list[i+1]]

            title = ok.split('#')[0]

            title = re.sub(r'([一二三四五六七八九十][\.、])|[:：]', '', title)
            content = ''.join(ok.split('#')[1:])
            results.append({'title': title, 'content': content})

        if not title_found:
            results.append({'title': None, 'content': purecontent})
        return results


if __name__ == '__main__':
    FineParse().parse_item_treatment()
