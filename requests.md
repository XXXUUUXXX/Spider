import requests
r = requests.get('http://www.baidu.com')
r.url #查看r所对应的url
r.status_code #查看对应http返回状态码
r.encoding #查看返回内容字符集
r.text #查看返回的内容，会根据响应的头的字符集编码做动态调整
r.content #以字节的方式响应内容，如img类型的字节流
r.json() #内置的JSON解码器
r.headers #查看以一个Python字典形式展示的服务器响应头，根据 RFC 2616 ， HTTP头部是大小写不敏感的。
r.request.headers #查看请求头
r.headers.get('content-type') #获取content-type对应的值
r.cookies['example_cookie_name']查看cookies信息，注意写法，是key value形式
r.history #查看请求历史

请求超时设置：
仅对连接过程有效，与响应体的下载无关
requests.get('http://www.baidu.com', timeout=0.001) 

响应的迭代器：
默认情况下，当你进行网络请求后，响应体会立即被下载。你可以通过stream参数覆盖这个行为，推迟下载响应体直到访问 Response.content 属性:
r = requests.get('http://www.baidu.com', stream=True) 
for line in r.iter_lines():
    print line

Session会话保持：
s = requests.Session()
s.get('http://www.baidu.com') #两次请求，系统会认为是一个user登录
s.get('http://www.baidu.com')

POST请求
import requests
s = requests.Session()
s.get("http://uliweb.cpython.org")
token = s.cookies["_csrf_token"]
d ={"csrf_token":token,
    "username":"python",
    "password":"python"}
r = s.post("http://uliweb.cpython.org/login",data=d)
print r.content


Upgrade-Insecure-Requests：参数为1。该指令用于让浏览器自动升级请求从http到https,用于大量包含http资源的http网页直接升级到https而不会报错。简洁的来讲,就相当于在http和https之间起的一个过渡作用。就是浏览器告诉服务器，自己支持这种操作，我能读懂你服务器发过来的上面这条信息，并且在以后发请求的时候不用http而用https；

User-Agent：有一些网站不喜欢被爬虫程序访问，所以会检测连接对象，如果是爬虫程序，也就是非人点击访问，它就会不让你继续访问，所以为了要让程序可以正常运行，我们需要设置一个浏览器的User-Agent；

Accept：浏览器可接受的MIME类型，可以根据实际情况进行设置；

Accept-Encoding：浏览器能够进行解码的数据编码方式，比如gzip。Servlet能够向支持gzip的浏览器返回经gzip编码的HTML页面。许多情形下这可以减少5到10倍的下载时间；

Accept-Language：浏览器所希望的语言种类，当服务器能够提供一种以上的语言版本时要用到；

Cookie：这是最重要的请求头信息之一。中文名称为“小型文本文件”或“小甜饼“，指某些网站为了辨别用户身份而储存在用户本地终端（Client Side）上的数据（通常经过加密）。定义于RFC2109。是网景公司的前雇员卢·蒙特利在1993年3月的发明。