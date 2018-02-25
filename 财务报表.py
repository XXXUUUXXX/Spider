# -*- coding:utf-8 -*-

import re
import sys
import json
import pymysql
import requests
from lxml import etree
from bs4 import BeautifulSoup


class Financial_Data(object):
    """获取财务数据"""

    def __init__(self):
        self.server = 'http://quotes.money.163.com/'
        self.cwsj = 'http://quotes.money.163.com/hkstock/cwsj_'
        # 主要财务指标
        self.cwzb_dict = {
            'YEAREND_DATE':'报表日期','EPS':'基本每股收益','EPS_DILUTED':'摊薄每股收益',
            'GROSS_MARGIN':'毛利率','LOANS_DEPOSITS':'贷款回报率','ROTA':'总资产收益率','ROEQUITY':'净资产收益率',
            'CURRENT_RATIO':'流动比率','QUICK_RATIO':'速动比率','CAPITAL_ADEQUACY':'资本充足率',
            'TOTAL_ASSET2TURNOVER':'资产周转率','ROLOANS':'存贷比','INVENTORY_TURNOVER':'存货周转率',
            'GENERAL_ADMIN_RATIO':'管理费用比率','FINCOSTS_GROSSPROFIT':'财务费用比率','TURNOVER_CASH':'销售现金比率'
        }
        # 利润表
        self.lrb_dict = {
            'YEAREND_DATE':'报表日期','TURNOVER':'总营收','INCOME_INTEREST':'利息收益',
            'INCOME_NETFEE':'费用收益','OPER_PROFIT':'经营利润','PBT':'除税前利润','NET_PROF':'净利润',
            'EPS':'每股基本盈利','DPS':'每股派息','INCOME_NETTRADING':'交易收益'
        }
        # 资产负债表
        self.fzb_dict = {
            'YEAREND_DATE':'报表日期','FIX_ASS':'固定资产','CURR_ASS':'流动资产','CURR_LIAB':'流动负债',
            'INVENTORY':'存款','CASH':'现金及银行存结','OTHER_ASS':'其他资产',
            'CASH_SHORTTERMFUND':'库存现金及短期资金','DEPOSITS_FROM_CUSTOMER':'客户存款',
            'LOAN_TO_BANK':'银行同业存款及贷款','FINANCIALASSET_SALE':'可供出售之证券',
            'DERIVATIVES_ASSET':'金融资产','DERIVATIVES_LIABILITIES':'金融负债',
            'TOTAL_ASS':'总资产','TOTAL_LIAB':'总负债','EQUITY':'股东权益'
        }
        # 现金流量表
        self.llb_dict = {
            'YEAREND_DATE':'报表日期','CF_NCF_OPERACT':'经营活动产生的现金流','CF_INT_REC':'已收利息',
            'CF_INT_PAID':'已付利息','CF_INT_REC':'已收股息','CF_DIV_PAID':'已派股息',
            'CF_INV':'投资活动产生现金流','CF_FIN_ACT':'融资活动产生现金流',
            'CF_BEG':'期初现金及现金等价物','CF_CHANGE_CSH':'现金及现金等价物净增加额',
            'CF_END':'期末现金及现金等价物','CF_EXCH':'汇率变动影响',
        }
        # 总表
        self.table_dict = {'cwzb': self.cwzb_dict,'lrb': self.lrb_dict, 'fzb': self.fzb_dict, 'llb': self.llb_dict}
        self.headers = {
            'Connection': 'keep-alive'
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

    def get_informations(self, url):
        """获取页面信息"""

        request = requests.get(url = url, headers = self.headers)
        request.encoding = 'utf-8'
        html = request.text
        #page_bf = BeautifulSoup(html, 'lxml')
        content = etree.HTML(html)
        # 股票民称
        name = content.xpath('//span[@class="name"]')[0]
        # 存储各个表名的列表
        table_name_list = []
        table_date_list = []
        each_date_list = []
        url_list = []
        table_name = content.xpath('')


    def insert_tables(self, name, table_name_list, table_date_list, url_list):
        # 打开数据库连接 host-连接主机地址 port-端口号 user-用户名 passwd-密码 db-数据库名 charset-编码
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='tian1538', db='financial_data', charset='utf-8')
        # 使用cursor()方法操作游标
        cursor = conn.cursor()
        # 写入信息
        for i in range(len(table_name_list)):
            sys.stdout.write('正在下载%s' % table_name_list[i] + '\r')
            # 获取数据地址
            url = self.server + 'hk/service/cwsj_service.php?symbol={}&start={}&end={}&type={}'.for

#http://quotes.money.163.com/hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=cwzb

#http://quotes.money.163.com/hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=lrb&#unit=yuan

#http://quotes.money.163.com/hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=fzb&unit=yuan

#http://quotes.money.163.com/hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=llb&unit=yuan