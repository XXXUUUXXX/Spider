# -*- coding:utf-8 -*-

import requests
from lxml import etree
from bs4 import BeautifulSoup
import subprocess as sp
import random
import re


def get_proxies(page = 1):
    """
    获取西刺高匿代理
    Parameters:
        page: 高匿代理页数，默认第一页
    Returns:
        proxies_list: 代理列表
    """

    # requests的Session可以自动保持cookie
    S = requests.Session()
    url = 'http://www.xicidaili.com/nn/%d' % page
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.xicidaili.com/nn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    # get请求
    response = S.get(url = url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text

    ip_list_bf1 = BeautifulSoup(html, 'lxml')
    ip_list_bf2 = BeautifulSoup(str(ip_list_bf1.find_all(id = 'ip_list')), 'lxml')
    ip_list_info = ip_list_bf2.table.contents 

    # 用来存储代理的列表
    proxies_list = []
    for index in range(len(ip_list_info)):
        if index % 2 == 1 and index != 1: # 奇数下标
            dom = etree.HTML(str(ip_list_info[index]))
            ip = dom.xpath('//td[2]')[0]
            port = dom.xpath('//td[3]')[0]
            protocol = dom.xpath('//td[6]')[0]
            proxies_list.append(protocol.text.lower() + "#" + ip.text + '#' + port.text)
    print(proxies_list)
    return proxies_list


def check_ip(ip, lose_time, waste_time):
    """
    检查代理的连通性
    Parameters:
        ip: ip地址
        lose_time: 匹配丢包数
        waste_time: 匹配平均时间
    Returns:
        average_time: 代理ip平均耗时
    """

    # 命令 -n 要发送的回显请求数 -w等待每次回复的超时时间(毫秒)
    cmd = 'ping -n 3 -w 3 %s'
    # 执行命令
    # Subprocess.Popen()可以创建一个进程，当shell参数为true时，程序通过shell来执行
    # stdin,stdout,stderr分别表示程序的标准输入，输出，错误句柄
    p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    # 获得返回结果并解码
    out = p.stdout.read().decode("gbk")
    # 丢包数
    lose_time = lose_time.findall(out)
    # 当匹配到丢失包信息失败，默认为三次请求全部丢包，丢包数lose赋值为3
    if len(lose_time) == 0:
        lose = 3
    else:
        lose = int(lose_time[0])
    # 如果丢包数大于2个，则认为连接超时，返回平均耗时1000ms
    if lose > 2:
        return 1000 # 返回False
    else:
        # 平均时间
        average = waste_time.findall(out)
        # 当匹配耗时时间信息失败，默认三次请求严重超时，返回平均耗时时间1000ms
        if len(average) == 0:
            return 1000
        else:
            average_time = int(average[0])
            return average_time

def init_pattern():
    """
    初始化正则表达式
    Parameters: 无
    Returns:
        lose_time: 匹配丢包数
        waste_time: 匹配平均时间
    """

    # 匹配丢包数
    lose_time = re.compile(u'丢失 = (\d+)', re.IGNORECASE)
    # 匹配平均时间
    waste_time = re.compile(u'平均 = (\d+)ms', re.IGNORECASE)
    return lose_time, waste_time

if __name__ == '__main__':
    # 初始化正则表达式
    lose_time, waste_time = init_pattern()
    # 获取ip代理
    proxies_list = get_proxies(1)

    # 如果平均时间超过200ms重新选取ip
    while True:
        # 从100个ip中随机选取一个ip作为代理访问
        proxy = random.choice(proxies_list)
        split_proxy = proxy.split('#')
        ip = split_proxy[1]
        # 检查ip
        average_time = check_ip(ip, lose_time, waste_time)
        if average_time > 200:
            # 删除不能使用的ip
            proxies_list.remove(proxy)
            print('ip连接超时，重新获取。。。')
        else:
            break
    # 删除已经在使用的ip
    proxies_list.remove(proxy)
    proxy_dict = {split_proxy[0]:split_proxy[1] + ':' + split_proxy[2]}
    print('正在使用代理', proxy_dict)