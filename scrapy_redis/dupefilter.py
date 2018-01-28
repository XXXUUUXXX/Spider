# -*- coding:utf-8 -*-

import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from BloomfilterOnRedis import BloomFilter

from . import connection


class RFPDupeFilter(BaseDupeFilter):
    def __init__(self, server, key):
        self.server = server
        self.key = key
        self.bf = BloomFilter(server, key, blockNum=1) # 如果url比较多可以增加blockNum

    @classmethod
    def from_settings(cls, settings):

        server = connection.from_settings_filter(settings)
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.bf.isContains(fp):  # 如果已经存在
            return True
        else:
            self.bf.insert(fp)
            return False
        # This returns the number of values added, zero if already exists.
        #added = self.server.sadd(self.key, fp)
        #return added == 0

    def close(self, reason=''):
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)
