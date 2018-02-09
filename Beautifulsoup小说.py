#-*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup

class Downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.url = 'http://www.biqukan.com/1_1094/'
        self.names = []  # 章节名
        self.urls = []  # 章节链接
        self.nums = 0  # 章节数

    def get_url(self):
        """获取下载链接"""
        request = requests.get(url=self.url)
        html = request.text
        # find_all方法的第一个参数是获取的标签名
        # 第二个参数class_是标签的属性，class_防止和关键字冲突
        # find_all匹配的返回结果是一个列表
        div_bf = BeautifulSoup(html, 'lxml')  # div标签
        div = div_bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]), 'lxml')  # a标签
        print(a_bf)
        a = a_bf.find_all('a')
        self.nums = len(a[15:])  # 剔除前几个无用章节
        # .get获取属性值   .string获取标签名
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, url):
        """获取章节内容"""
        request = requests.get(url = url)
        html = request.text
        bf = BeautifulSoup(html, 'lxml')
        texts = bf.find_all('div', class_ = 'showtxt')
        # 提取匹配结果后，使用text属性，提取文本内容，滤除br标签
        # replace方法剔除空格，替换为回车
        # &nbsp;在html中用来表示空格
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    def write_contents(self, name, path, text):
        """写入文件"""
        with open(path, 'a', encoding='utf-8') as f:
            # 写入的顺序：章节名->内容->2个换行
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == '__main__':
    dl = Downloader()
    dl.get_url()
    print('开始下载。。。')
    for i in range(dl.nums):
        dl.write_contents(dl.names[i], '一念永恒.txt', dl.get_contents(dl.urls[i]))
        # 把调试中打印的信息保存到文件中，多线程日志中用sys.stdout.write来封装日志写入
        sys.stdout.write('已下载:%.3f%%' % float(i/dl.nums*100) + '\r') # 保留三位小数，回车
        # 刷新输出
        sys.stdout.flush()
    print('下载完成。。。')