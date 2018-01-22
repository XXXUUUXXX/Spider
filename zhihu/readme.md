原作者：AlexTan 
Github: https://github.com/AlexTan-b-z


学习学习
环境：windows
软件： redis，mongodb,phantomjs
模块：scrapy，scrapy-redis,selenium，pymongo
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



通过fiddler抓包的body为3000左右
%2C是用URL编码形式表示的ASCII字符'逗号,'

https://www.zhihu.com/api/v4/members/peng-dong-cheng-38?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cincluded_answers_count%2Cincluded_articles_count%2Cincluded_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cis_org_createpin_white_user%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics
--------------------------------简化提取需要的url-------------------------------------------------
https://www.zhihu.com/api/v4/members/peng-dong-cheng-38?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge%5B%3F(type%3Dbest_answerer)%5D.topics