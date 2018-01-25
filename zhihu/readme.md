原作者：AlexTan 
Github: https://github.com/AlexTan-b-z


学习学习
环境：windows
软件： redis，mongodb,phantomjs
模块：scrapy，scrapy-redis,selenium，pymongo，pytesseract
python3安装scrapy
python3 -m pip install scrapy


使用：
在cookie.py中填入知乎账号密码
运行：scrapy crawl zhihuspider
分布式扩展：将代码拷贝到新机器，修改settings.py中REDIS_HOST和FILTER_HOST,改为主机ip地址


支持断点续爬
分布式
去重
支持手动识别验证码和自动识别验证码，自动登录需购买云打码账号，默认手动
增加机器识别


通过fiddler抓包的body为3000左右
%2C是用URL编码形式表示的ASCII字符'逗号,'
简化URL用URL解码工具http://tool.chinaz.com/tools/urlencode.aspx

start_requests-->parse-->parse_relation-->parse

多个item


时间戳变时间
import time

timestamp = 1500449608
time_local = time.localtime(timestamp)
time_local = time.strftime('%Y-%m-%d %H:%M:%S', time_local)
print time_local

time_c = one['created_time']
item['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_c))
time_u = one['updated_time']
item['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_u))
