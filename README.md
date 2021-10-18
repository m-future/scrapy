<!--
 * @Author: mfuture@qq.com
 * @Date: 2021-10-12 13:08:44
 * @Description: 
 * @FilePath: /health39/README.md
-->

# 简介

## 1. 框架

- [scrapy](https://docs.scrapy.org/en/latest/index.html)
- scrapy list # 查看项目中的爬虫列表
- scrapy genspider (name) (domain) # 新建一个爬虫
- scrapy crawl (name) # 运行某个爬虫

## 2. 项目中爬虫作用如下

- department: 获取[39健康网](https://jbk.39.net/)上的科室，便于后面爬疾病时使用
- disease: 获取39健康网上的疾病及其相关信息
- ipproxy: 获取第三方[供应商](http://www.feidudaili.com/index/gratis/index)的代理ip, 在middlewares 里面设置开启代理

## 3. 设置

- 在settings.py设置 USE_IP_PROXY 来决定是否使用代理（默认使用）

## 4. 命令行使用

- scrapy crawl disease 运行disease这个爬虫
- python3 jbk39/lib/network.py 可以更新代理IP的可用性
- ```ctrl+z``` 暂停爬虫
- jobs 查看当前任务
- bg 后台运行
- fg 恢复运行
- kill %num 杀死进程
- 删除jobs里面的对应文件夹，才能重新运行一个爬虫，否则视为任务已完成
