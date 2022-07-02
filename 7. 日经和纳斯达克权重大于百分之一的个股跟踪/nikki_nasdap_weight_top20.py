
#! -*- coding:utf-8 -*-


import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 正则和lxml混用
def naspda_parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！

    selector = etree.HTML(html)
    Price = selector.xpath('//*[@id="spFP"]/div[1]/span[1]/text()')
    for item in Price:
        big_list.append(item)

def nikki_parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！

    selector = etree.HTML(html)
    now_price = selector.xpath('//*[@id="stockinfo_i1"]/div[2]/span[2]/text()')
    f_price = RemoveDot(remove_block(now_price))
    big_list.append(f_price[0])



def RemoveDot(item):
    f_l = []
    for it in item:

        f_str = "".join(it.split(",")).split("円")[0]
        f_l.append(f_str)

    return f_l




def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items






def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Trust',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:

        f_104 = "%s," *46
        cursor.executemany('insert into top20_nasdap_nikki (_AAPL,_MSFT,_AMZN,_TSLA,_GOOG,_GOOGL,_META,_NVDA,_PEP,_COST,_AVGO,_CSCO,_CMCSA,_ADBE,_TMUS,_INTC,_QCOM,_TXN,_AMGN,_AMD,_HON,_INTU,J9983,J8035,J9984,J9433,J6367,J6954,J4543,J4063,J6857,J6971,J6762,J6098,J6758,J7733,J4503,J7203,J4519,J4568,J7832,J9613,J2413,J6988,J9735,J9766) values ({0})'.format(f_104[:-1]), content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    big_list = []
    nasdap100_top20 = "AAPL,MSFT,AMZN,TSLA,GOOG,GOOGL,META,NVDA,PEP,COST,AVGO,CSCO,CMCSA,ADBE,TMUS,INTC,QCOM,TXN,AMGN,AMD,HON,INTU"
    f_nasdap100_top20 =nasdap100_top20.split(",")
    for code in f_nasdap100_top20:
        url = "http://gu.qq.com/us{0}.OQ/gg".format(code)
        html = call_page(url)
        print(url)
        naspda_parse_html(html)
    jl_string = "9983,8035,9984,9433,6367,6954,4543,4063,6857,6971,6762,6098,6758,7733,4503,7203,4519,4568,7832,9613,2413,6988,9735,9766"
    jl=jl_string.split(",")
    for item in jl:
        url = 'https://kabutan.jp/stock/chart?code={0}'.format(item)
        html = call_page(url)
        print(url)

        nikki_parse_html(html)

    ff_l = []
    f_tup = tuple(big_list)
    ff_l.append((f_tup))
    print(ff_l)
    insertDB(ff_l)

 # create table top20_nasdap_nikki (id int not null primary key auto_increment, _AAPL text,_MSFT text,_AMZN text,_TSLA text,_GOOG text,_GOOGL text,_META text,_NVDA text,_PEP text,_COST text,_AVGO text,_CSCO text,_CMCSA text,_ADBE text,_TMUS text,_INTC text,_QCOM text,_TXN text,_AMGN text,_AMD text,_HON text,_INTU text,J9983 text,J8035 text,J9984 text,J9433 text,J6367 text,J6954 text,J4543 text,J4063 text,J6857 text,J6971 text,J6762 text,J6098 text,J6758 text,J7733 text,J4503 text,J7203 text,J4519 text,J4568 text,J7832 text,J9613 text,J2413 text,J6988 text,J9735 text,J9766 text, LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ) engine=InnoDB  charset=utf8;
