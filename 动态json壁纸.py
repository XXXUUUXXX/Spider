# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
# closing()把任意对象变为上下文对象,如果一个对象没有实现上下文，就不能用于with语句
from contextlib import closing 


class Photos(object):
    def __init__(self):
        self.photos_id = []
        self.download_url = 'https://unsplash.com/photos/photo_id/download?force=true'
        self.url = 'https://unsplash.com/napi/feeds/home'
        self.headers = {
                'Authorization': 'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

    def get_ids(self):
        """获取图片id"""
        request = requests.get(url = self.url, headers = self.headers)
        # 转换为python格式
        html = json.loads(request.text)
        next_page = html['next_page']
        for each in html['photos']:
            self.photos_id.append(each['id'])
        time.sleep(1)
        for i in range(5):
            request = requests.get(url = next_page, headers = self.headers)
            html = json.loads(request.text)
            next_page = html['next_page']
            for each in html['photos']:
                self.photos_id.append(each['id'])
            time.sleep(1)

    def download(self, photo_id, filename):
        """下载图片"""
        url = self.download_url.replace('photo_id', photo_id)
        # stream=True,默认情况下，当你进行网络请求后，响应体会立即被下载，通过stream参数覆盖这个行为，推迟下载响应体直到访问response.content属性
        with closing(requests.get(url = url, stream = True, headers = self.headers)) as r:
            with open('%d.jpg' % filename, 'ab+') as f: # ab+表示以二进制格式打开一个文件用于追加，如果文件已经存在，文件指针将会放在文件的结尾
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
if __name__ == '__main__':
    p = Photos( )
    p.get_ids()
    print('图片下载中。。。')
    for i in range(len(p.photos_id)):
        print('正在下载第%张图片'% (i+1))
        p.download(p.photos_id[i], (i+1))


