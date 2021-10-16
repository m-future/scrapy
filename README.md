<!--
 * @Author: mfuture@qq.com
 * @Date: 2021-10-12 13:08:44
 * @LastEditTime: 2021-10-12 13:48:13
 * @LastEditors: mfuture@qq.com
 * @Description: 
 * @FilePath: /jbk39/README.md
-->

#### 1. 本项目使用 [scrapy](https://docs.scrapy.org/en/latest/index.html) 爬虫框架
- scrapy list # 查看项目中的爬虫列表
- scrapy genspider spidername # 新建一个爬虫
- scrapy crawl spidername # 运行某个爬虫


#### 2. 项目中爬虫作用如下：
- department: 获取[39健康网](https://jbk.39.net/)上的科室，便于后面爬疾病时使用
- disease: 获取39健康网上的疾病及其相关信息
- ipproxy: 获取第三方[供应商](http://www.feidudaili.com/index/gratis/index)的代理ip, 在middlewares 里面设置开启代理
