from bs4 import BeautifulSoup
from io import BytesIO
import pycurl
import time
import re
# ==============================<<Web>>==============================
def getContent(url,encoding='utf-8'): 
    # 只回传网页内容
    curl=pycurl.Curl()
    buf=BytesIO()
    content=''

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.CONNECTTIMEOUT, 60)
    curl.setopt(pycurl.HEADER, True)
    curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    curl.setopt(pycurl.AUTOREFERER,1)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)

    try:
        curl.perform()  
        content=buf.getvalue().decode(encoding,'ignore')
        buf.close()
        curl.close()

    except pycurl.error:
        print("Connection was reset.")
    finally:
        traceback.print_exc()
        writeText(traceback.format_exc(),'PyCrawler-Log.txt')

    return content

def postContent(url,post,encoding='utf-8'):
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE,1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    #crl.setopt(pycurl.AUTOREFERER,1)
    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    #crl.setopt(pycurl.PROXY,proxy)
    crl.setopt(pycurl.HTTPPROXYTUNNEL,1)
    #crl.setopt(pycurl.NOSIGNAL, 1)

    crl.fp = BytesIO()
    crl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")

    # Option -d/--data <data>  HTTP POST data
    crl.setopt(crl.POSTFIELDS, urllib.parse.urlencode(post))
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)

    try:
        crl.perform()
        content=crl.fp.getvalue().decode(encoding,'ignore')

    except pycurl.error:
        print("Connection was reset.")
    
    finally:
        traceback.print_exc()
        writeText(traceback.format_exc(),'PyCrawler-Log.txt') 

    return content;

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

# ==============================<<IO>>==============================

def writeText(tmp,filename):
    try:
        with open('E:\\Yue\\PY\\data\\'+filename, 'a+', encoding='utf-8') as f:
            f.write(str(tmp))
            f.write('\r\n')
    except:
        traceback.print_exc()
        writeText(traceback.format_exc(),'PyCrawler-Log.txt')

    return;

def createDict(name,header,val):
    inst=dict.fromkeys(header) # 使用key建立dict
    it = iter(list(val)) # 产生值的iterator
    for key in header:
        inst[key]=next(it)
    return {name:inst} # 加上省份法院

def appendix(name,filename):
    strr='['+name+']'
    strr=strr+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    writeText(strr,filename)
    print(strr)

    return;

def parseLinks(class_name,tmp): # 从网页中截取sub-link, 天津 吉林
    soup=BeautifulSoup(tmp, 'html.parser')
    Links=[]
    for span in soup.find_all(class_=class_name):  # 依照class, <a href=''> 抓link
        for link in span.find_all('a'):
            Links.append(link.get('href'))
    return Links

def parseList(strr): #解析成dic
    dic={}
    if re.findall('http://\S+?\'',strr):
        dic['网址']=re.findall('http://\S+?\'',strr)[0].replace('\'','')

    if re.search('[、，。（）\w]+?一案',strr):
        dic['公告正文']=re.search('[、，。（）\w]+?一案',strr).group() 
    elif re.search('\w+开庭审理',strr):
        dic['公告正文']=re.search('\w+开庭审理',strr).group()
    elif re.search('我院[、，。（）\w]+?',strr):
        dic['公告正文']=re.search('我院[、，。（）\w]+?',strr).group()
    else:
        dic['公告正文']=''

    if re.search('2016-\d+-\d+',strr):
        dic['发布时间']=re.search('2016-\d+-\d+',strr).group()
    elif re.search('二〇一六年\w+月\w+日{0,1}',strr):
        dic['发布时间']=re.search('二〇一六年\w+月\w+日{0,1}',strr).group()

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
        print('NoneType')

    return unified;

def getDicLst(key,filename): # 回传除重后dic组成的list
    buf=str()
    result=[]
    dic={}

    with open('E:\Yue\PY\data\\'+filename,'r',encoding='utf-8') as f:
        buf=re.sub('\s+','',f.read())
        # 去空白
        buf=re.sub('\[\w{2,3}\]','',buf)
        buf=re.sub('\[[-:\d]+?\]','',buf)
        # 除去Appendix

    for item in deDuplicate(key,buf): 
        dic=parseList(item)
        result.append(dic)

    print('Set size:',len(result))

    return result;