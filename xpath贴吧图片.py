# -*- coding:utf-8 -*-

import urllib
import urllib2
from lxml import etree

def load_page(url):
    """
        作用：根据url发送请求，获取服务器响应文件
        url：爬取的url地址
        filename：处理的文件名
    """
    #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    # 解析HTML文档为HTML DOM模型
    content = etree.HTML(html)
    # 返回所有匹配成功的列表集合
    link_list = content.xpath('//div[@class="t_con cleafix"]//div/div/a/@href')
    for link in link_list:
        # 组合链接
        fulllink = "http://tieba.baidu.com" + link
        load_Image(fulllink)
        #print fulllink

# 取出每个帖子里面的每个图片链接
def load_Image(link):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    request = urllib2.Request(link, headers = headers)
    response = urllib2.urlopen(request)
    html = response.read()
    # 解析
    content = etree.HTML(html)
    # 取出帖子里每层层主发送的图片链接集合
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    # 获取图片的链接
    for link in link_list:
        write_Image(link)
        #print link

def write_Image(link):
    """
        作用：将html内容写入本地
        link：图片链接
    """
    # 文件写入
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    request = urllib2.Request(link, headers = headers)
    # 图片原始数据
    image = urllib2.urlopen(request).read()
    # 取后十位作为文件名
    filename = link[-10:]
    # 写入本地磁盘
    with open(filename, "wb") as f:
        f.write(image)
    print "成功下载" + filename

def tieba_spider(url, begin_page, end_page):
    """
        作用：贴吧爬虫调度器，负责组合处理每个页面的url
        url：贴吧url的前部分
        begin_page：起始页
        end_page：结束页
    """
    for page in range(begin_page, end_page + 1):
        pn = (page - 1) * 50
        fullurl = url + "&pn=" + str(pn)
        load_page(fullurl)

if __name__ == '__main__':
    kw = raw_input("输入要爬取的贴吧名字：")
    begin_page = int(raw_input("输入起始页："))
    end_page = int(raw_input("输入结束页："))

    url = "http://tieba.baidu.com/f?"
    key = urllib.urlencode({"kw": kw})
    fullurl = url + key
    tieba_spider(fullurl, begin_page, end_page)