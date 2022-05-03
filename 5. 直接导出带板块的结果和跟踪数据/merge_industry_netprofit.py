# js   js_infos_finandata
# coding industry title market
import csv
import os

import pandas as pd
import pymysql
import datetime



def merge_industryPlusNetProfits(select_string):

    select_string = select_string.split(",")
    # count top 30

    three_table_title = ["one_stock", "title_zh_cn", "industry_infos", "sector_infos", "current_dt",
                         "current_dt_minus1", "current_dt_minus2", "current_dt_minus3", "current_dt_minus4",
                         "sina_stock_url", "infos_zh_cn"]

    writeinto_detail(csvfilename, three_table_title)

    for one_stock in select_string:
    # get netprofits
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='ForLynne',
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cur = connection.cursor()
        # sql 语句
        sql_netprofits = "select name,current_dt,current_dt_minus1,current_dt_minus2,current_dt_minus3,current_dt_minus4,sina_stock_url from sp_nas_netprofits_fromsina  where code = '{0}'   ".format(
            one_stock)
        cur.execute(sql_netprofits)
        # #获取所有记录列表
        data_sql_netprofits = cur.fetchone()
        current_dt = data_sql_netprofits["current_dt"]
        current_dt_minus1 = data_sql_netprofits["current_dt_minus1"]
        current_dt_minus2 = data_sql_netprofits["current_dt_minus2"]
        current_dt_minus3 = data_sql_netprofits["current_dt_minus3"]
        current_dt_minus4 = data_sql_netprofits["current_dt_minus4"]
        sina_stock_url = data_sql_netprofits["sina_stock_url"]

    # get industry data
        sql_industry_info = "select title_zh_cn,industry_infos,sector_infos,infos_zh_cn from spplusnas_industry_infos where code = '{0}'   ".format(
            one_stock)
        cur.execute(sql_industry_info)
        # #获取所有记录列表
        sql_industry_info = cur.fetchone()
        print(sql_industry_info)
        title_zh_cn = sql_industry_info["title_zh_cn"]
        industry_infos = sql_industry_info["industry_infos"]
        sector_infos = sql_industry_info["sector_infos"]
        infos_zh_cn = sql_industry_info["infos_zh_cn"]
        three_table_info = [one_stock,title_zh_cn,industry_infos,sector_infos,current_dt,current_dt_minus1,current_dt_minus2,current_dt_minus3,current_dt_minus4,sina_stock_url,infos_zh_cn]
        writeinto_detail(csvfilename, three_table_info)
        cur.close()


def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8-sig") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)

def csv2excel(csvfilename,excelname):
    #1 csv--> excel
    #2. remove csv
    data_csv = pd.read_csv(csvfilename)
    data_csv.to_excel(excelname)
    os.remove(csvfilename)

if __name__== "__main__":
    sp500_plus_nas100_forDB = "AAPL,A,AAL,AAP,ABBV,ABC,ABMD,ABT,ACN,ADBE,ADI,ADM,ADP,ADS,ADSK,AEE,AEP,AES,AFL,AIG,AIV,AIZ,AJG,AKAM,ALB,ALGN,ALK,ALL,ALLE,ALXN,AMAT,AMCR,AMD,AME,AMGN,AMP,AMT,AMZN,ANET,ANSS,ANTM,AON,AOS,APA,APD,APH,APTV,ARE,ASML,ATO,ATVI,AVB,AVGO,AVY,AWK,AXP,AZO,BA,BAC,BAX,BBY,BDX,BEN,BF.B,BIDU,BIIB,BK,BKNG,BKR,BLK,BLL,BMRN,BMY,BR,BRK.B,BSX,BWA,BXP,C,CAG,CAH,CARR,CAT,CB,CBOE,CBRE,CCI,CCL,CDNS,CDW,CE,CERN,CF,CFG,CHD,CHKP,CHRW,CHTR,CI,CINF,CL,CLX,CMA,CMCSA,CME,CMG,CMI,CMS,CNC,CNP,COF,COG,COO,COP,COST,COTY,CPB,CPRT,CRM,CSCO,CSGP,CSX,CTAS,CTL,CTSH,CTVA,CTXS,CVS,CVX,CXO,D,DAL,DD,DE,DFS,DG,DGX,DHI,DHR,DIS,DISCA,DISCK,DISH,DLR,DLTR,DOV,DOW,DPZ,DRE,DRI,DTE,DUK,DVA,DVN,DXC,DXCM,EA,EBAY,ECL,ED,EFX,EIX,EL,EMN,EMR,EOG,EQIX,EQR,ES,ESS,ETFC,ETN,ETR,EVRG,EW,EXC,EXPD,EXPE,EXR,F,FANG,FAST,FB,FBHS,FCX,FDX,FE,FFIV,FIS,FISV,FITB,FLIR,FLS,FLT,FMC,FOX,FOXA,FRC,FRT,FTI,FTNT,FTV,GD,GE,GILD,GIS,GL,GLW,GM,GOOG,GOOGL,GPC,GPN,GPS,GRMN,GS,GWW,HAL,HAS,HBAN,HBI,HCA,HD,HES,HFC,HIG,HII,HLT,HOG,HOLX,HON,HPE,HPQ,HRB,HRL,HSIC,HST,HSY,HUM,HWM,IBM,ICE,IDXX,IEX,IFF,ILMN,INCY,INFO,INTC,INTU,IP,IPG,IPGP,IQV,IR,IRM,ISRG,IT,ITW,IVZ,J,JBHT,JCI,JD,JKHY,JNJ,JNPR,JPM,JWN,K,KEY,KEYS,KHC,KIM,KLAC,KMB,KMI,KMX,KO,KR,KSS,KSU,L,LB,LBTYA,LBTYK,LDOS,LEG,LEN,LH,LHX,LIN,LKQ,LLY,LMT,LNC,LNT,LOW,LRCX,LULU,LUV,LVS,LW,LYB,LYV,MA,MAA,MAR,MAS,MCD,MCHP,MCK,MCO,MDLZ,MDT,MELI,MET,MGM,MHK,MKC,MKTX,MLM,MMC,MMM,MNST,MO,MOS,MPC,MRK,MRO,MS,MSCI,MSFT,MSI,MTB,MTD,MU,MXIM,MYL,NBL,NCLH,NDAQ,NEE,NEM,NFLX,NI,NKE,NLOK,NLSN,NOC,NOV,NOW,NRG,NSC,NTAP,NTES,NTRS,NUE,NVDA,NVR,NWL,NWS,NWSA,NXPI,O,ODFL,OKE,OMC,ORCL,ORLY,OTIS,OXY,PAYC,PAYX,PBCT,PCAR,PEAK,PEG,PEP,PFE,PFG,PG,PGR,PH,PHM,PKG,PKI,PLD,PM,PNC,PNR,PNW,PPG,PPL,PRGO,PRU,PSA,PSX,PVH,PWR,PXD,PYPL,QCOM,QRVO,RCL,RE,REG,REGN,RF,RHI,RJF,RL,RMD,ROK,ROL,ROP,ROST,RSG,RTX,SBAC,SBUX,SCHW,SEE,SGEN,SHW,SIRI,SIVB,SJM,SLB,SLG,SNA,SNPS,SO,SPG,SPGI,SPLK,SRE,STE,STT,STX,STZ,SWK,SWKS,SYF,SYK,SYY,T,TAP,TCOM,TDG,TEL,TFC,TFX,TGT,TIF,TJX,TMO,TMUS,TPR,TROW,TRV,TSCO,TSLA,TSN,TT,TTWO,TWTR,TXN,TXT,UA,UAA,UAL,UDR,UHS,ULTA,UNH,UNM,UNP,UPS,URI,USB,V,VAR,VFC,VIAC,VLO,VMC,VNO,VRSK,VRSN,VRTX,VTR,VZ,WAB,WAT,WBA,WDAY,WDC,WEC,WELL,WFC,WHR,WLTW,WM,WMB,WMT,WRB,WRK,WST,WU,WY,WYNN,XEL,XLNX,XOM,XRAY,XRX,XYL,YUM,ZBH,ZBRA,ZION,ZTS"
    time_ = datetime.datetime.now().strftime("%Y-%m-%d")
    csvfilename ="industryInfo-NetProfits-spplusnas.csv"
    excelname ="industryInfo-NetProfits-spplusnas.xlsx".format(time_)
    merge_industryPlusNetProfits(sp500_plus_nas100_forDB)
    csv2excel(csvfilename, excelname)