#! -*- coding:utf-8 -*-


import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver


def use_selenium_headless(url):
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



def use_requests(url):
    response = requests.get(url)
    return response.text

def getinfos_fromGoogleFinance(code):
    url = "https://www.google.com/finance/quote/{0}:NASDAQ?hl=zh-CN".format(code)
    html = use_requests(url)
    selector = etree.HTML(html)
    title_zh_cn = selector.xpath('//*[@id="yDmH0d"]/c-wiz/div/div[4]/div/div/main/div[1]/div[2]/text()')
    pattern = re.compile('<div class="bLLb2d">(.*?)<a target="_blank" rel=".*?" href=".*?" class=".*?">Wikipedia</a>',re.S)
    infos_zh_cn = re.findall(pattern,html)
    return title_zh_cn,infos_zh_cn







def getinfos_fromYhaooFinance(code):
    url = "https://finance.yahoo.com/quote/{0}/profile?p={0}".format(code)
    html = use_selenium_headless(url)
    selector = etree.HTML(html)
    industry_infos = selector.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()')
    sector_infos = selector.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]/text()')
    return industry_infos,sector_infos





def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='ForLynne',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into spplusnas_industry_infos (code,title_zh_cn,industry_infos,sector_infos,infos_zh_cn) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass

def remove_list(item):
    if item == []:
        item = [""]
        result = item
    else:
        result = item
    return result


if __name__ == '__main__':
    big_list = []
    sp500_plus_nas100_industry = "AAPL,A,AAL,AAP,ABBV,ABC,ABMD,ABT,ACN,ADBE,ADI,ADM,ADP,ADS,ADSK,AEE,AEP,AES,AFL,AIG,AIV,AIZ,AJG,AKAM,ALB,ALGN,ALK,ALL,ALLE,ALXN,AMAT,AMCR,AMD,AME,AMGN,AMP,AMT,AMZN,ANET,ANSS,ANTM,AON,AOS,APA,APD,APH,APTV,ARE,ASML,ATO,ATVI,AVB,AVGO,AVY,AWK,AXP,AZO,BA,BAC,BAX,BBY,BDX,BEN,BF.B,BIDU,BIIB,BK,BKNG,BKR,BLK,BLL,BMRN,BMY,BR,BRK.B,BSX,BWA,BXP,C,CAG,CAH,CARR,CAT,CB,CBOE,CBRE,CCI,CCL,CDNS,CDW,CE,CERN,CF,CFG,CHD,CHKP,CHRW,CHTR,CI,CINF,CL,CLX,CMA,CMCSA,CME,CMG,CMI,CMS,CNC,CNP,COF,COG,COO,COP,COST,COTY,CPB,CPRT,CRM,CSCO,CSGP,CSX,CTAS,CTL,CTSH,CTVA,CTXS,CVS,CVX,CXO,D,DAL,DD,DE,DFS,DG,DGX,DHI,DHR,DIS,DISCA,DISCK,DISH,DLR,DLTR,DOV,DOW,DPZ,DRE,DRI,DTE,DUK,DVA,DVN,DXC,DXCM,EA,EBAY,ECL,ED,EFX,EIX,EL,EMN,EMR,EOG,EQIX,EQR,ES,ESS,ETFC,ETN,ETR,EVRG,EW,EXC,EXPD,EXPE,EXR,F,FANG,FAST,FB,FBHS,FCX,FDX,FE,FFIV,FIS,FISV,FITB,FLIR,FLS,FLT,FMC,FOX,FOXA,FRC,FRT,FTI,FTNT,FTV,GD,GE,GILD,GIS,GL,GLW,GM,GOOG,GOOGL,GPC,GPN,GPS,GRMN,GS,GWW,HAL,HAS,HBAN,HBI,HCA,HD,HES,HFC,HIG,HII,HLT,HOG,HOLX,HON,HPE,HPQ,HRB,HRL,HSIC,HST,HSY,HUM,HWM,IBM,ICE,IDXX,IEX,IFF,ILMN,INCY,INFO,INTC,INTU,IP,IPG,IPGP,IQV,IR,IRM,ISRG,IT,ITW,IVZ,J,JBHT,JCI,JD,JKHY,JNJ,JNPR,JPM,JWN,K,KEY,KEYS,KHC,KIM,KLAC,KMB,KMI,KMX,KO,KR,KSS,KSU,L,LB,LBTYA,LBTYK,LDOS,LEG,LEN,LH,LHX,LIN,LKQ,LLY,LMT,LNC,LNT,LOW,LRCX,LULU,LUV,LVS,LW,LYB,LYV,MA,MAA,MAR,MAS,MCD,MCHP,MCK,MCO,MDLZ,MDT,MELI,MET,MGM,MHK,MKC,MKTX,MLM,MMC,MMM,MNST,MO,MOS,MPC,MRK,MRO,MS,MSCI,MSFT,MSI,MTB,MTD,MU,MXIM,MYL,NBL,NCLH,NDAQ,NEE,NEM,NFLX,NI,NKE,NLOK,NLSN,NOC,NOV,NOW,NRG,NSC,NTAP,NTES,NTRS,NUE,NVDA,NVR,NWL,NWS,NWSA,NXPI,O,ODFL,OKE,OMC,ORCL,ORLY,OTIS,OXY,PAYC,PAYX,PBCT,PCAR,PEAK,PEG,PEP,PFE,PFG,PG,PGR,PH,PHM,PKG,PKI,PLD,PM,PNC,PNR,PNW,PPG,PPL,PRGO,PRU,PSA,PSX,PVH,PWR,PXD,PYPL,QCOM,QRVO,RCL,RE,REG,REGN,RF,RHI,RJF,RL,RMD,ROK,ROL,ROP,ROST,RSG,RTX,SBAC,SBUX,SCHW,SEE,SGEN,SHW,SIRI,SIVB,SJM,SLB,SLG,SNA,SNPS,SO,SPG,SPGI,SPLK,SRE,STE,STT,STX,STZ,SWK,SWKS,SYF,SYK,SYY,T,TAP,TCOM,TDG,TEL,TFC,TFX,TGT,TIF,TJX,TMO,TMUS,TPR,TROW,TRV,TSCO,TSLA,TSN,TT,TTWO,TWTR,TXN,TXT,UA,UAA,UAL,UDR,UHS,ULTA,UNH,UNM,UNP,UPS,URI,USB,V,VAR,VFC,VIAC,VLO,VMC,VNO,VRSK,VRSN,VRTX,VTR,VZ,WAB,WAT,WBA,WDAY,WDC,WEC,WELL,WFC,WHR,WLTW,WM,WMB,WMT,WRB,WRK,WST,WU,WY,WYNN,XEL,XLNX,XOM,XRAY,XRX,XYL,YUM,ZBH,ZBRA,ZION,ZTS"
    list_sp500_plus_nas100_industry =sp500_plus_nas100_industry.split(",")
    for code in list_sp500_plus_nas100_industry:
        title_zh_cn,infos_zh_cn = getinfos_fromGoogleFinance(code)
        industry_infos,sector_infos = getinfos_fromYhaooFinance(code)

        s_item = [code] + remove_list(title_zh_cn)+ remove_list(industry_infos)+ remove_list(sector_infos)+remove_list(infos_zh_cn)
        print(code,title_zh_cn,industry_infos,sector_infos,infos_zh_cn)
        f_tuple = tuple(s_item)
        finanl_content = [f_tuple]
        insertDB(finanl_content)


# select code,title_zh_cn,infos_zh_cn from SpPlusNas_industry_infos where code = "AAPL"  ;
# select code,infos_zh_cn from SpPlusNas_industry_infos where id >=1 and id >10;



#  Lynne@$$


# create table spplusnas_industry_infos
# (id int not null primary key auto_increment,
# code  text,
# title_zh_cn text,
# industry_infos text,
# sector_infos text,
# infos_zh_cn  text,
# LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;

# drop table SpPlusNas_industry_infos;