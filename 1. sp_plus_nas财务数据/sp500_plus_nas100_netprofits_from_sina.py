# -*- coding:utf-8 -*-
import datetime
import re
import time
import pymysql
from lxml import etree
from selenium import webdriver


#http://chromedriver.storage.googleapis.com/index.html
# centos chrome
#https://jingyan.baidu.com/article/03b2f78c546d951fa237ae99.html

#google-chrome --version

def get_first_page(url):
    ch_options = webdriver.ChromeOptions()
    # 为Chrome配置无头模式
    ch_options.add_argument("--headless")
    ch_options.add_argument('--no-sandbox')
    ch_options.add_argument('--disable-gpu')
    ch_options.add_argument('--disable-dev-shm-usage')
    # 在启动浏览器时加入配置
    driver = webdriver.Chrome(options=ch_options)
    driver.get(url)
    html = driver.page_source
    # driver.quit()
    return html



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='ForLynne',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into sp_nas_netprofits_fromsina (code,name,current_dt,current_dt_minus1,current_dt_minus2,current_dt_minus3,current_dt_minus4,sina_stock_url) values (%s,%s,%s,%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


if __name__ == '__main__':
    sp500_plus_nas100_forNetProfits = "AAPL,A,AAL,AAP,ABBV,ABC,ABMD,ABT,ACN,ADBE,ADI,ADM,ADP,ADS,ADSK,AEE,AEP,AES,AFL,AIG,AIV,AIZ,AJG,AKAM,ALB,ALGN,ALK,ALL,ALLE,ALXN,AMAT,AMCR,AMD,AME,AMGN,AMP,AMT,AMZN,ANET,ANSS,ANTM,AON,AOS,APA,APD,APH,APTV,ARE,ASML,ATO,ATVI,AVB,AVGO,AVY,AWK,AXP,AZO,BA,BAC,BAX,BBY,BDX,BEN,BF.B,BIDU,BIIB,BK,BKNG,BKR,BLK,BLL,BMRN,BMY,BR,BRK.B,BSX,BWA,BXP,C,CAG,CAH,CARR,CAT,CB,CBOE,CBRE,CCI,CCL,CDNS,CDW,CE,CERN,CF,CFG,CHD,CHKP,CHRW,CHTR,CI,CINF,CL,CLX,CMA,CMCSA,CME,CMG,CMI,CMS,CNC,CNP,COF,COG,COO,COP,COST,COTY,CPB,CPRT,CRM,CSCO,CSGP,CSX,CTAS,CTL,CTSH,CTVA,CTXS,CVS,CVX,CXO,D,DAL,DD,DE,DFS,DG,DGX,DHI,DHR,DIS,DISCA,DISCK,DISH,DLR,DLTR,DOV,DOW,DPZ,DRE,DRI,DTE,DUK,DVA,DVN,DXC,DXCM,EA,EBAY,ECL,ED,EFX,EIX,EL,EMN,EMR,EOG,EQIX,EQR,ES,ESS,ETFC,ETN,ETR,EVRG,EW,EXC,EXPD,EXPE,EXR,F,FANG,FAST,FB,FBHS,FCX,FDX,FE,FFIV,FIS,FISV,FITB,FLIR,FLS,FLT,FMC,FOX,FOXA,FRC,FRT,FTI,FTNT,FTV,GD,GE,GILD,GIS,GL,GLW,GM,GOOG,GOOGL,GPC,GPN,GPS,GRMN,GS,GWW,HAL,HAS,HBAN,HBI,HCA,HD,HES,HFC,HIG,HII,HLT,HOG,HOLX,HON,HPE,HPQ,HRB,HRL,HSIC,HST,HSY,HUM,HWM,IBM,ICE,IDXX,IEX,IFF,ILMN,INCY,INFO,INTC,INTU,IP,IPG,IPGP,IQV,IR,IRM,ISRG,IT,ITW,IVZ,J,JBHT,JCI,JD,JKHY,JNJ,JNPR,JPM,JWN,K,KEY,KEYS,KHC,KIM,KLAC,KMB,KMI,KMX,KO,KR,KSS,KSU,L,LB,LBTYA,LBTYK,LDOS,LEG,LEN,LH,LHX,LIN,LKQ,LLY,LMT,LNC,LNT,LOW,LRCX,LULU,LUV,LVS,LW,LYB,LYV,MA,MAA,MAR,MAS,MCD,MCHP,MCK,MCO,MDLZ,MDT,MELI,MET,MGM,MHK,MKC,MKTX,MLM,MMC,MMM,MNST,MO,MOS,MPC,MRK,MRO,MS,MSCI,MSFT,MSI,MTB,MTD,MU,MXIM,MYL,NBL,NCLH,NDAQ,NEE,NEM,NFLX,NI,NKE,NLOK,NLSN,NOC,NOV,NOW,NRG,NSC,NTAP,NTES,NTRS,NUE,NVDA,NVR,NWL,NWS,NWSA,NXPI,O,ODFL,OKE,OMC,ORCL,ORLY,OTIS,OXY,PAYC,PAYX,PBCT,PCAR,PEAK,PEG,PEP,PFE,PFG,PG,PGR,PH,PHM,PKG,PKI,PLD,PM,PNC,PNR,PNW,PPG,PPL,PRGO,PRU,PSA,PSX,PVH,PWR,PXD,PYPL,QCOM,QRVO,RCL,RE,REG,REGN,RF,RHI,RJF,RL,RMD,ROK,ROL,ROP,ROST,RSG,RTX,SBAC,SBUX,SCHW,SEE,SGEN,SHW,SIRI,SIVB,SJM,SLB,SLG,SNA,SNPS,SO,SPG,SPGI,SPLK,SRE,STE,STT,STX,STZ,SWK,SWKS,SYF,SYK,SYY,T,TAP,TCOM,TDG,TEL,TFC,TFX,TGT,TIF,TJX,TMO,TMUS,TPR,TROW,TRV,TSCO,TSLA,TSN,TT,TTWO,TWTR,TXN,TXT,UA,UAA,UAL,UDR,UHS,ULTA,UNH,UNM,UNP,UPS,URI,USB,V,VAR,VFC,VIAC,VLO,VMC,VNO,VRSK,VRSN,VRTX,VTR,VZ,WAB,WAT,WBA,WDAY,WDC,WEC,WELL,WFC,WHR,WLTW,WM,WMB,WMT,WRB,WRK,WST,WU,WY,WYNN,XEL,XLNX,XOM,XRAY,XRX,XYL,YUM,ZBH,ZBRA,ZION,ZTS"
    list_sp500_plus_nas100_forNetProfits = sp500_plus_nas100_forNetProfits.split(",")
    for url_code in list_sp500_plus_nas100_forNetProfits:
        print(url_code)
        big_list = []
        last_list = []
        big_list.append(url_code)
        url_f = 'http://quotes.sina.com.cn/usstock/hq/income.php?s=' + str(url_code) +'&t=quarter'
        html = get_first_page(url_f)
        selector = etree.HTML(html)
        name = selector.xpath('/html/body/div[2]/div[5]/h3/text()')
        profits = selector.xpath('/html/body/div[2]/div[7]/div[2]/table[2]/tbody/tr[15]/td/text()')
        sina_stock_url = "https://stock.finance.sina.com.cn/usstock/quotes/{0}.html".format(url_code)
        contents = name + profits + [sina_stock_url]
        big_tuple_list = list(contents)
        for i in big_tuple_list:
            b = "".join(re.split(r'亿|万|\s', i))  # 同时去除了空格，亿，万３个标签
            big_list.append(b)

        big_list_tuple = tuple(big_list)
        last_list.append(big_list_tuple)
        print(last_list)
        insertDB(last_list)
        print(datetime.datetime.now())
        time.sleep(0.1)




# create table sp_nas_netprofits_fromsina(
# id int not null primary key auto_increment,
# code varchar(10),
# name varchar(80),
# current_dt varchar(10),
# current_dt_minus1 varchar(10),
# current_dt_minus2 varchar(10),
# current_dt_minus3 varchar(10),
# current_dt_minus4 varchar(10),
# sina_stock_url text
#  ) engine=InnoDB default charset=utf8;

#
# drop table sp_nas_netprofits_fromsina;


# Lynne@$$
# a= ['6亿','6万','8亿']
# t = []
# for i in a:
#     b = "".join(re.split(r'亿|万|\s',a))
#     t.append(b)
#
# print(t)  # t = [6,6,8]
