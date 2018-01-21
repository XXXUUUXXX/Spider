手机抓包：

Fiddler
Options中打钩
-->HTTPS-->（Capture HTTPS CONNECTs,Decrypt HTTPS traffic, Ignore server certificate errors）
Actions选中Reset All Certificates
-->Connections--> (Allow remote computers to connect,Reuse client connections,Reuse server connections)

下载安全证书，在浏览器中输入http://localhost:8888/，下载FiddlerRoot certificate
将安全证书拷贝到手机中安装，(小米mix2为例)设置-->更多设置-->系统安全-->从存储设备安装

手机和电脑共用一个路由器或者电脑开房wifi热点，手机连入
在手机的WLAN中点击当前wifi，代理设置为手动，主机名为电脑端IP，端口为8888

在fiddler中左侧点击一条数据，右侧GET获取URL，POST获取json