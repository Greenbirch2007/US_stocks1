# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import pymysql
import pandas as pd

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime

engine_Nas_Mons = create_engine('mysql+pymysql://root:123456@localhost:3306/Trust')


sql_Nas_Mons = 'select * from top20_nasdap_nikki  ; '

ln = os.getcwd()


def savedt():

    df_js225 = pd.read_sql_query(sql_Nas_Mons, engine_Nas_Mons)
    excelFile3 = '{0}/{1}.xlsx'.format(ln, "top20_nasdap_nikki")  # 处理了文件属于当前目录下！
    df_js225.to_excel(excelFile3)





if __name__ == '__main__':
    savedt()