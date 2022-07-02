

# IW ---SN
# 3----254
import string
import time
# -*- coding: utf-8 -*-

# 读取页面文本
# 按照标题，保存整个文本





import csv
import datetime

import os
import re
import time
import sys
type = sys.getfilesystemencoding()
import pymysql
import xlrd
import requests
from requests.exceptions import RequestException
from lxml import etree

# 1. 先读取excel文件中列数，然后+1，列数*2-1
# 2. 相对为位置
# 3.然后直接使用


def removeDot(item):
    f_l = []
    for it in item:
        f_str = "".join(it.split(","))
        f_l.append(f_str)

    return f_l


def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items



# print(sh.nrows)#有效数据行数
# print(sh.ncols)#有效数据列数
# print(sh.cell(0,0).value)#输出第一行第一列的值
# print(sh.row_values(0))#输出第一行的所有值
# #将数据和标题组合成字典
# print(dict(zip(sh.row_values(0),sh.row_values(1))))
# #遍历excel，打印所有数据
# for i in range(sh.nrows):
#     print(sh.row_values(i))





ff_List=[]
alphabet =string.ascii_uppercase
head_str='Public num As Integer\nSub s()\nDim i As Integer\nFor i = 2 To 9999\nIf Range("C" & i) = "" Then\nnum = i\nExit For\nEnd If'
tail_str='Next\nRange("{0}1:{1}" & num).Select\nActiveSheet.Shapes.AddChart2(227, xlLine).Select\nActiveChart.SetSourceData Source:=Range("Sheet1!${0}$1:${1}$" & num)\nEnd Sub'
str_1 = ' Range("{0}1").Select\nActiveCell.FormulaR1C1 = "=RC[-{2}]"\nRange("{0}" & i).Select \n ActiveCell.FormulaR1C1 = "=RC[-{2}]/R2C{1}-1"'




for i1 in alphabet:
    ff_List.append(i1)
    for i2 in alphabet:
        f_al =i1+i2
        ff_List.append(f_al)




def into_file(f_name,item_name):
    try:
        with open('{0}.bas'.format(f_name), 'a') as file_handle:

            file_handle.write(item_name + "")  # 写入
            file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据
            print("{0} 整理完毕".format(f_name))
    except:
        pass




if __name__=="__main__":

    # 先按照字符串长度排序(小->大)，再按照字母排序
    f_alist=sorted(ff_List, key=lambda i: len(i), reverse=False)
    # 1.读取excel文件

    # 打开excel
    wb = xlrd.open_workbook('top20_nasdap_nikki.xlsx')
    # 按工作簿定位工作表
    sh = wb.sheet_by_name('Sheet1')
    f_ncols = sh.ncols
    # start_index1 = f_alist.index("W")  # 修改处1
    # end_index1 = f_alist.index("AN")  # 修改处2
    start_index = f_ncols + 1
    end_index = f_ncols * 2-3
    len_str = end_index - start_index + 3



    into_file("F_js20210608_top10",head_str)
    for a_i,num in zip(f_alist[start_index:end_index+1],range(3,end_index-start_index+3+1)):

        f_code=str_1.format(a_i,num,len_str)
        into_file("F_js20210608_top10",f_code)

    into_file("F_js20210608_top10", tail_str.format(f_alist[start_index],f_alist[end_index]))