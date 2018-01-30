# -*- coding: utf-8 -*-



from scrapy import Item, Field

# 用户个人信息
class ZhihuItem(Item):
    # 用户id
    user_id = Field()
    # 头像链接
    user_image_url = Field()
    # 用户名称
    name = Field()
    # 性别
    gender = Field()
    # 居住地
    locations = Field()
    # 所在行业
    business = Field()
    # 职业经历
    employments = Field()
    # 教育经历
    educations = Field()
    # 关注人数
    followees_num = Field()
    # 粉丝人数
    followers_num = Field()

# 关系
class RelationItem(Item):
    # 用户id
    user_id = Field()
    # 关系类型
    relation_type = Field()
    # 关系人的id
    relations_id = Field()

# 回答
class AnswerItem(Item):
    # 回答的用户
    answer_user_id = Field()
    # 回答内容的id
    answer_id = Field()
    # 问题的id
    question_id = Field()
    # 创建的时间
    created_time = Field()
    # 更新的时间
    updated_time = Field()
    # 赞成数量
    voteup_count = Field()
    # 评论数量
    comment_count = Field()
    # 回答内容
    content = Field()

# 提问
class QuestionItem(Item):
    # 提问人的id
    ask_user_id = Field()
    # 问题的id
    question_id = Field()
    # 提问时间
    ask_time = Field()
    # 回答数量
    answer_count = Field()
    # 关注数量
    followees_count = Field()
    # 提问标题
    title = Field()

# 文章
class ArticleItem(Item):
    # 作者id
    author_id = Field()
    # 文章标题
    title = Field()
    # 文章id
    article_id = Field()
    # 内容
    content = Field()
    # 创建时间
    created_time = Field()
    # 更新时间
    updated_time = Field()
    # 赞成数量
    voteup_count = Field()
    # 评论数量
    comment_count = Field()


