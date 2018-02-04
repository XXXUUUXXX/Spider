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