# -*- coding: utf-8 -*-

import scrapy
import os
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ImagesPipeline(ImagesPipeline):
    #def process_item(self, item, spider):
    #    return item

    # 获取settings文件里设置的变量值
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    # 该方法的作用：为每一个图片链接生成一个Request对象，该方法的输出作为item_completed的输入中的results
    # results是一个元组，每个元组包括(success, imageinfoorfailure),如果success=true，imageinfoor_failure是一个字典，包括url/path/checksum三个key。
    def get_media_requests(self, item, info):
        image_url = item['imagelink']
        yield scrapy.Request(image_url)

    def item_completed(self, result, item, info):
        # 固定写法，获取图片路径并判断路径是否正确，如果正确就放到image_path里面
        image_path = [x["path"] for ok, x in result if ok]

        os.rename(self.IMAGES_STORE + "/" + image_path[0], self.IMAGES_STORE + "/" + item["nickname"] + ".jpg")
        item['imagePath'] = self.IMAGES_STORE +'/' + item['nickname']

        return item