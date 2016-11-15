# coding=utf-8
# 将html格式的表格转换成单纯的row, 有gbk编码问题
from bs4 import BeautifulSoup
import re
from MajorCrawler import *
#------------------------------------------------------------------------

def createDict(name,header,val):
    inst=dict.fromkeys(header) # 使用key建立dict
    it = iter(list(val)) # 产生值的iterator
    for key in header:
        inst[key]=next(it)
    return {name:inst} # 加上省份法院

def initial_DB(db_name,coll_name,host="localhost",port=27017):
    import pymongo
    client=pymongo.MongoClient(host,port)
    db=client[db_name]
    coll=db[coll_name]
    return coll

def insert_Doc(coll,doc):
    doc_id = coll.insert(doc)
    return doc_id

#------------------------------------------------------------------------

def parseShanghai():
    # Query包含重复的header, 记得到Robomongo去移除
    # db.getCollection('Shanghai_Hign_People_Court').find({"上海市高级人民法院.案由" : "案由"})
    
    db_name='Public_Info_Nov16'
    coll_name='Shanghai_Court'
    header=["法院","法庭","开庭日期","案号","案由","承办部门","审判长/主审人","原告/上诉人","被告/被上诉人"] 
    #样本

    text_file=open("E:\Yue\PY\data\Shanghai.txt",encoding='utf-8',errors='ignore')
    text_query=text_file.read()
    text_file.close()
    # ---------开启网页原始挡案---------

    count=error=0
    soup=BeautifulSoup(text_query, 'html.parser')
    coll=initial_DB(db_name,coll_name)
    # 不要用html5Parser, 效能差

    for table in soup.find_all("tbody"):
        try:
            for row in table.find_all('tr'):
                cells = row.find_all(re.compile('td'))
                print("Parsing cells ...")
                if len(cells)==9:
                    List=[]
                    for i in range(0,9):
                        List.append(cells[i].find(text=True).replace('\xa0','')) # '\xa0'为GBK无法解析的空白

                    tmp=createDict("上海市高级人民法院",header,List)
                    insert_Doc(coll,tmp)
                    count+=1
                else:
                    error+=1
        except:
            content

    print("上海 is finished.")
    print("Summary(count,error): ",count,", ",error)

def deDuplicate(key,src): #透过set除重
    unified=set()
    lst=re.findall(key,src)

    if lst:
        for node in lst: unified.add(node)
    else:
        print('NoneType')

    return unified;

def deduction(key,filename): # 产生filename_d.txt
    buf=str()
    result=[]
    with open('E:\Yue\PY\data\\'+filename,'r',encoding='utf-8') as f:
        buf=re.sub('\s+','',f.read())
        # 去空白
        buf=re.sub('\[\w{2,3}\]','',buf)
        buf=re.sub('\[[-:\d]+?\]','',buf)
        # 除去Appendix

    for item in deDuplicate(key,buf): 
        result.append(item)
        #将去重后的再次加入list

    print('de: ',len(result))

    for ele in result:
        writeText(ele,'\de\\'+filename.replace('.txt','_d.txt'))

    return;

#------------------------------------------------------------------------


parseShanghai()