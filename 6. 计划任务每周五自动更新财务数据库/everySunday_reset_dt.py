

import os
import pymysql

connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='ForLynne',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
cursor.execute('drop table sp_nas_netprofits_fromsina;')
print('删表成功！')
cursor.execute('create table sp_nas_netprofits_fromsina(id int not null primary key auto_increment,code varchar(10),name varchar(80),current_dt varchar(10),current_dt_minus1 varchar(10),current_dt_minus2 varchar(10),current_dt_minus3 varchar(10),current_dt_minus4 varchar(10),sina_stock_url text) engine=InnoDB default charset=utf8;')
connection.commit()
connection.close()
print('建表成功！')

os.system("python3 sp500_plus_nas100_netprofits_from_sina.py")


#  * 6  * * * /usr/bin/python3 /root/everySunday_reset_dt.py
