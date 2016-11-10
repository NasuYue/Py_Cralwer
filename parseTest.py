#encoding=utf8
from MajorCrawler import *

# ==============================<<DB>>==============================
def initial_DB(db_name,coll_name,host="localhost",port=27017):
    import pymongo
    client=pymongo.MongoClient(host,port)
    db=client[db_name]
    coll=db[coll_name]
    return coll

def insert_Doc(coll,doc):
    doc_id = coll.insert(doc)
    return doc_id

def parseList(strr): #解析成dic
    dic={}

    if re.findall('\[(http\S+?)\]',strr):
        dic['网址']=re.findall('\[(http\S+?)\]',strr)[0]
    if re.findall('http://\S+?\'l',strr):
        dic['网址']=re.findall('(http://\S+?)\'',strr)[0]

    if re.search('[：、，。（）()\w]+?一案',strr):
        dic['公告正文']=re.search('[：、，。（）()\w]+?一案',strr).group() 
    elif re.search('\w+开庭审理',strr):
        dic['公告正文']=re.search('\w+开庭审理',strr).group()
    elif re.search('我院[：、，。（）()\w]+?',strr):
        dic['公告正文']=re.search('我院[：、，。（）()\w]+?',strr).group()
    else:
        dic['公告正文']=''

    if re.search('2016-\d+-\d+',strr):
        dic['发布时间']=re.search('2016-\d+-\d+',strr).group()
    elif re.search('二〇一六年\w+月\w+日{0,1}',strr):
        dic['发布时间']=re.search('二〇一六年\w+月\w+日{0,1}',strr).group()
    elif re.search('定于20\d\d年\d+月\d+日',strr):
        dic['发布时间']=re.search('20\d\d年\d+月\d+日',strr).group()
    else:
        dic['发布时间']=''

    if re.search('[\d\w()]+?号',strr):
        dic['案号']=re.search('[\d\w()]+?号',strr).group()

    if re.search('\w+?法院',strr):
        dic['法院']=re.search('\w+?法院',strr).group() 

    return dic

def createDict(name,header,val):
    inst=dict.fromkeys(header) # 使用key建立dict
    it = iter(list(val)) # 产生值的iterator
    for key in header:
        inst[key]=next(it)
    return {name:inst} # 加上省份法院

def deDuplicate(key,src): #透过set除重
    unified=set()
    lst=re.findall(key,src)

    if lst: #如果key找得到, 加入set
        for node in lst:
            unified.add(node)
    else:
        print('NoneType: Regular key is not work.')

    return unified;

def getDictLst(key,filename,flag): # 回传除重后dic组成的list
    buf=str()
    result=[]
    dic={}
    
    with open('E:\Yue\PY\data\\'+filename,'r',encoding='utf-8') as f:
        buf=re.sub('\s+','',f.read())
        buf=re.sub('\[\w{2,3}\]','',buf)
        buf=re.sub('\[[-:\d\s]+?\]','',buf)
        # 除去Appendix

    for item in deDuplicate(key,buf):
        if flag==0: # list
            dic= parseList(item)

        elif flag==1: # node
            link=re.findall('\[(http\S+?)\]',item)[0] if re.findall('\[(http\S+?)\]',item) else ''
            node=re.sub('\[http\S+?\]','',item)
            dic={'网址':link , '内容':node}

        elif flag==2: # dict
            dic=eval(item)

        else:
            print('Flag is not define:',flag)

        result.append(dic)

    print('Set:',len(result))

    return result;

def access(key,coll_name,db_name,court_name,filename,flag):
    dicList=getDictLst(key,filename,flag)
    coll=initial_DB(db_name,coll_name)

    for item in dicList:
        insert_Doc(coll,{court_name:item})

    print('Insertions:', len(dicList), '\r\n')

    return;

# ==============================<<Instance>>==============================

db_name='Public_Info_Nov16'
dic={
    '北京市': 'Beijing', '河北省': 'Hebei', '吉林省': 'Jilin', '甘肃省': 'Gansu', '湖北省': 'Hubei', 
    '安徽省': 'Anhui', '辽宁省': 'Liaoning', '山东省': 'Shandong', '广东省': 'Guangdong', '河南省': 'Henan', 
    '浙江省': 'Zhejiang', '宁夏回族自治区': 'Ningxia', '云南省': 'Yunnan', '重庆市': 'Chongqing', '江西省': 'Jiangxi', 
    '贵州省': 'Guizhou', '海南省': 'Hainan', '青海省': 'Qinhai', '湖南省': 'Hunan', '内蒙古自治区': 'InnerMongolia', 
    '天津市': 'Tianjin', '福建省': 'Fujian', '上海市': 'Shanghai'}

# flag=0
lst_Key={
    '辽宁省':'\[[\S]+?\]', '海南省':'\[[\S]+?\]', '湖南省':'\[[\S]+?\]', '甘肃省':'\[[\S]+?\]', 
    '宁夏回族自治区':'\[[\S]+?\]', '青海省':'\[[\S]+?\]', '福建省':'\[[\S]+?\]', '北京市':'\[[\S]+?\]'
}

# flag=1
node_Key={
    '安徽省':'<divstyle=\"text-align:center\">[\S]+?\]', '重庆市':'<tbody>[\S]+?\]', 
    '内蒙古自治区':'<divclass="ywzw_con_inner">[\S]+?\]','河北省':'<divclass="ywzw_con_inner">[\S]+?</div>',
    '云南省':'<divclass="ywzw_con_inner">[\S]+?\]', '贵州省':'<divstyle=\"min-height:400px;\">[\S]+?</div>',
    '天津市':'天津[\S]+?一案', '江西省':'\{[\S\s]+?\}', '吉林省':'<divclass=\"page\">[\S]+?</div>',
    '湖北省':'<divclass=\"ywzw_con_inner\">[\S]+?</div>', '广东省': '\[[\S]+?\]', '河南省': '<divclass="list">[\S]+?</div>',
    '上海市': '<TR>[\S]+?</TR>'
}

dic_key={
    '山东省':'\{[\S]+?\}', '浙江省': '\{[\S]+?\}'
}


for k,v in lst_Key.items():
    coll_name= dic[k]+'_Court'
    filename= dic[k]+'.txt'
    print('[',k,']')
    access(v,coll_name,db_name,k,filename,0)

for k,v in node_Key.items():
    coll_name= dic[k]+'_Court'
    filename= dic[k]+'.txt'
    print('[',k,']')
    access(v,coll_name,db_name,k,filename,1)


for k,v in dic_key.items():
    coll_name= dic[k]+'_Court'
    filename= dic[k]+'.txt'
    print('[',k,']')
    access(v,coll_name,db_name,k,filename,2)

# issue: 山东 北京