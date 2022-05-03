


import csv
import operator
import re
import time

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os

def remove_list(item):
    if item == []:
        item = [""]
        result = item
    else:
        result = item
    return result


def get_notnull_fromlist(list_content):
    result_list = []
    for item in list_content:
        if len(item) !=0:
            result_list.append(item)
    return result_list

def top2index_top30_and_last30_stock(db_tablename,dbname):
    # 1 首先前2位是股指,后面都是个股(计算好的超越贝塔的收益率数据)
# 2 先保证最近的50个个股不为空的数量大于三分之一
# 3 以最后一个收益率进行排序。输出代码和收益率
# 4 返回代码和带代码的收益率
    engine_Lynne_Mons = create_engine('mysql+pymysql://root:123456@localhost:3306/{0}'.format(dbname))
    sql_Mons = 'select * from {0}  ; '.format(db_tablename)
    df_sp_plus_nas = pd.read_sql_query(sql_Mons, engine_Lynne_Mons)
    sp500_plus_nas100_forDB = "INX,IXIC,AAPL,A,AAL,AAP,ABBV,ABC,ABMD,ABT,ACN,ADBE,ADI,ADM,ADP,ADS,ADSK,AEE,AEP,AES,AFL,AIG,AIV,AIZ,AJG,AKAM,ALB,ALGN,ALK,_ALL,ALLE,ALXN,AMAT,AMCR,AMD,AME,AMGN,AMP,AMT,AMZN,ANET,ANSS,ANTM,AON,AOS,APA,APD,APH,APTV,ARE,ASML,ATO,ATVI,AVB,AVGO,AVY,AWK,AXP,AZO,BA,BAC,BAX,BBY,BDX,BEN,BF_B,BIDU,BIIB,BK,BKNG,BKR,BLK,BLL,BMRN,BMY,BR,BRK_B,BSX,BWA,BXP,C,CAG,CAH,CARR,CAT,CB,CBOE,CBRE,CCI,CCL,CDNS,CDW,CE,CERN,CF,CFG,CHD,CHKP,CHRW,CHTR,CI,CINF,CL,CLX,CMA,CMCSA,CME,CMG,CMI,CMS,CNC,CNP,COF,COG,COO,COP,COST,COTY,CPB,CPRT,CRM,CSCO,CSGP,CSX,CTAS,CTL,CTSH,CTVA,CTXS,CVS,CVX,CXO,D,DAL,DD,DE,DFS,DG,DGX,DHI,DHR,DIS,DISCA,DISCK,DISH,DLR,DLTR,DOV,DOW,DPZ,DRE,DRI,DTE,DUK,DVA,DVN,DXC,DXCM,EA,EBAY,ECL,ED,EFX,EIX,EL,EMN,EMR,EOG,EQIX,EQR,ES,ESS,ETFC,ETN,ETR,EVRG,EW,EXC,EXPD,EXPE,EXR,F,FANG,FAST,FB,FBHS,FCX,FDX,FE,FFIV,FIS,FISV,FITB,FLIR,FLS,FLT,FMC,FOX,FOXA,FRC,FRT,FTI,FTNT,FTV,GD,GE,GILD,GIS,GL,GLW,GM,GOOG,GOOGL,GPC,GPN,GPS,GRMN,GS,GWW,HAL,HAS,HBAN,HBI,HCA,HD,HES,HFC,HIG,HII,HLT,HOG,HOLX,HON,HPE,HPQ,HRB,HRL,HSIC,HST,HSY,HUM,HWM,IBM,ICE,IDXX,IEX,IFF,ILMN,INCY,INFO,INTC,INTU,IP,IPG,IPGP,IQV,IR,IRM,ISRG,IT,ITW,IVZ,J,JBHT,JCI,JD,JKHY,JNJ,JNPR,JPM,JWN,K,_KEY,_KEYS,KHC,KIM,KLAC,KMB,KMI,KMX,KO,KR,KSS,KSU,L,LB,LBTYA,LBTYK,LDOS,LEG,LEN,LH,LHX,LIN,LKQ,LLY,LMT,LNC,LNT,LOW,LRCX,LULU,LUV,LVS,LW,LYB,LYV,MA,MAA,MAR,MAS,MCD,MCHP,MCK,MCO,MDLZ,MDT,MELI,MET,MGM,MHK,MKC,MKTX,MLM,MMC,MMM,MNST,MO,MOS,MPC,MRK,MRO,MS,MSCI,MSFT,MSI,MTB,MTD,MU,MXIM,MYL,NBL,NCLH,NDAQ,NEE,NEM,NFLX,NI,NKE,NLOK,NLSN,NOC,NOV,NOW,NRG,NSC,NTAP,NTES,NTRS,NUE,NVDA,NVR,NWL,NWS,NWSA,NXPI,O,ODFL,OKE,OMC,ORCL,ORLY,OTIS,OXY,PAYC,PAYX,PBCT,PCAR,PEAK,PEG,PEP,PFE,PFG,PG,PGR,PH,PHM,PKG,PKI,PLD,PM,PNC,PNR,PNW,PPG,PPL,PRGO,PRU,PSA,PSX,PVH,PWR,PXD,PYPL,QCOM,QRVO,RCL,RE,REG,REGN,RF,RHI,RJF,RL,RMD,ROK,ROL,ROP,ROST,RSG,RTX,SBAC,SBUX,SCHW,SEE,SGEN,SHW,SIRI,SIVB,SJM,SLB,SLG,SNA,SNPS,SO,SPG,SPGI,SPLK,SRE,STE,STT,STX,STZ,SWK,SWKS,SYF,SYK,SYY,T,TAP,TCOM,TDG,TEL,TFC,TFX,TGT,TIF,TJX,TMO,TMUS,TPR,TROW,TRV,TSCO,TSLA,TSN,TT,TTWO,TWTR,TXN,TXT,UA,UAA,UAL,UDR,UHS,ULTA,UNH,UNM,UNP,UPS,URI,USB,V,VAR,VFC,VIAC,VLO,VMC,VNO,VRSK,VRSN,VRTX,VTR,VZ,WAB,WAT,WBA,WDAY,WDC,WEC,WELL,WFC,WHR,WLTW,WM,WMB,WMT,WRB,WRK,WST,WU,WY,WYNN,XEL,XLNX,XOM,XRAY,XRX,XYL,YUM,ZBH,ZBRA,ZION,ZTS"
    list_sp500_plus_nas100_forSearch = sp500_plus_nas100_forDB.split(",")
    data_list = []
    # count top 30
    for one_stock in list_sp500_plus_nas100_forSearch:
        # 2 先保证最近的50个个股不为空的数量大于三分之一
        if df_sp_plus_nas[one_stock].tolist()[-50:].count("") < 15:
            # 这里只是比较提取,不做计算
        # 3 以最后一个收益率进行排序。输出代码和收益率
            last_value = df_sp_plus_nas[-1:][one_stock].tolist()
            new_dict = {"code": one_stock, "value": last_value}
            data_list.append(new_dict)


    # 上面排序取前30个标的
    sort_data_top30 = sorted(data_list, key=operator.itemgetter('value'), reverse=True)
    sort_data_last30 = sorted(data_list, key=operator.itemgetter('value'), reverse=False)




    top30_code_list =[x["code"] for x in sort_data_top30[:30]]
    last30_code_list =[x["code"] for x in sort_data_last30[:30]]
    top30_value_list =[x["value"] for x in sort_data_top30[:30]]
    last30_value_list =[x["value"] for x in sort_data_last30[:30]]
    # t ={"AAPL":88,"BABA":66}
    top30_item_dict = dict(zip(top30_code_list,top30_value_list))
    last30_item_dict = dict(zip(last30_code_list,last30_value_list))

    return top30_code_list,last30_code_list,top30_item_dict,last30_item_dict







def save_ontime_dt(selectcode_string,dbname,db_tablename,filename):
    engine_Lynne_Mons = create_engine('mysql+pymysql://root:123456@localhost:3306/{0}'.format(dbname))
    df_js_f = pd.read_sql_query('select {0} from {1}  ; '.format(selectcode_string,db_tablename), engine_Lynne_Mons)
    df_js_f.to_excel(filename)


def load_ontimedt_and_detailsDt(tablename,dbname):
    output_dt_use_code(top30_code_list, "top30", dbname, tablename)

def output_dt_use_code(code_list,dt_type,dbname,db_tablename):
    fordb_select_code = ",".join(code_list)
    engine_Mons = create_engine('mysql+pymysql://root:123456@localhost:3306/{0}'.format(dbname))
    sql_f = 'select {0} from {1}  ; '.format(fordb_select_code,db_tablename)
    df_f = pd.read_sql_query(sql_f, engine_Mons)
    df_f.to_excel("{0}-{1}.xlsx".format(dt_type,db_tablename))


def merge_industryPlusNetProfits_ontime(select_list):
    # count top 30
    # csv会继续插入，xlsx
    os.chdir(outfilepath)
    if os.path.exists(top30_csvname):
        os.remove(top30_csvname)

    three_table_title = ["one_stock","s_value","title_zh_cn", "industry_infos", "sector_infos", "current_dt",
                         "current_dt_minus1", "current_dt_minus2", "current_dt_minus3", "current_dt_minus4",
                         "sina_stock_url", "infos_zh_cn"]

    writeinto_detail(top30_csvname, three_table_title)

    for one_stock in select_list:



    # get industry data
        if one_stock not in ["IXIC","INX"]:
            # get netprofits
            try:
                connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='ForLynne',
                                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
                cur = connection.cursor()
                # sql 语句
                sql_netprofits = "select current_dt,current_dt_minus1,current_dt_minus2,current_dt_minus3,current_dt_minus4,sina_stock_url from sp_nas_netprofits_fromsina  where code = '{0}' ;  ".format(one_stock)
                cur.executemany(sql_netprofits)
                # #获取所有记录列表
                data_sql_netprofits = cur.fetchone()
                current_dt = data_sql_netprofits["current_dt"]
                current_dt_minus1 = data_sql_netprofits["current_dt_minus1"]
                current_dt_minus2 = data_sql_netprofits["current_dt_minus2"]
                current_dt_minus3 = data_sql_netprofits["current_dt_minus3"]
                current_dt_minus4 = data_sql_netprofits["current_dt_minus4"]
                sina_stock_url = data_sql_netprofits["sina_stock_url"]


                sql_industry_info = "select title_zh_cn,industry_infos,sector_infos from spplusnas_industry_infos where code = '{0}'   ".format(one_stock)
                cur.execute(sql_industry_info)
                # #获取所有记录列表
                sql_industry_info = cur.fetchone()
                print(sql_industry_info)
                title_zh_cn = sql_industry_info["title_zh_cn"]
                industry_infos = sql_industry_info["industry_infos"]
                sector_infos = sql_industry_info["sector_infos"]
                three_table_info = [title_zh_cn,one_stock,top30_item_dict[one_stock][0],industry_infos,sector_infos,current_dt,current_dt_minus1,current_dt_minus2,current_dt_minus3,current_dt_minus4,sina_stock_url]
                writeinto_detail(top30_csvname, three_table_info)
                cur.close()
            except TypeError as e:
                print(e)


# select current_dt,current_dt_minus1,current_dt_minus2,current_dt_minus3,current_dt_minus4,sina_stock_url from sp_nas_netprofits_fromsina  where code = 'UAL' ;
# ['UAL', 'MTB', 'IBM', 'WDC', 'ETN', 'SNA', 'AAL', 'LKQ', 'NUE', 'DOW', 'ITW', 'HPE', 'RHI', 'JCI', 'MAS', 'DAL', 'COF', 'CMI', 'SYF', 'HBAN', 'GPC', 'HST', 'ISRG', 'CFG', 'RL', 'MMC', 'PCAR', 'MNST', 'TJX', 'INX']
# ['FTI', 'PSX', 'SYF', 'CFG', 'IXIC', 'INX']
# select industry_infos,sector_infos from spplusnas_industry_infos where code = 'INX'  ;


def mkdir(path):
    lpath = os.getcwd()
    isExists = os.path.exists(lpath + "/" + path)
    if not isExists:
        os.makedirs(path)


def writeinto_detail(filename,data):
    filenamepath = os.path.join(outfilepath, filename)
    with open(filenamepath,"a",newline="",encoding="utf-8-sig") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)



def csv2excel(csvfilename,excelname):
    #1 csv--> excel
    #2. remove csv
    os.chdir(outfilepath)
    data_csv = pd.read_csv(csvfilename)
    data_csv.to_excel(excelname)
    os.remove(csvfilename)

if __name__== "__main__":
    # 这里导出top30,last30数据
    mkdir("ForLynne_daily_dt")
    outfilepath = os.path.join(os.getcwd(), "ForLynne_daily_dt")
    dbname = "ForLynne"
    db_tablename ='following_sp500_plus_nas100_20220412'
    csvfilename = "{0}.csv".format(db_tablename)
    excelname = "{0}.xlsx".format(db_tablename)
    top30_csvname= "top30-{0}".format(re.sub("following_","",csvfilename))
    top30_excelname= "top30-{0}".format(re.sub("following_","",excelname))
    top30_code_list, last30_code_list, top30_item_dict, last30_item_dict = top2index_top30_and_last30_stock(db_tablename,dbname)
    # 1.得到top30 的板块数据，比单纯板块增加一个收益率 ok
    print(top30_code_list)
    get_notnull_fromlist_top30_code = get_notnull_fromlist(top30_code_list)
    merge_industryPlusNetProfits_ontime(get_notnull_fromlist_top30_code)
    # 2. top30 的实时数据导出 ，便于作图，去除0
    output_dt_use_code(get_notnull_fromlist_top30_code,"top30",dbname,db_tablename)
    csv2excel(top30_csvname, top30_excelname)

