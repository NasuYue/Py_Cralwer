#encoding=utf8
from bs4 import BeautifulSoup
from io import BytesIO
import traceback
import pycurl
import urllib
import json
import time
import re
# ==============================<<公用函式>>==============================

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
        writeText(traceback.format_exc(),'_ErrorLog.txt')

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
        writeText(traceback.format_exc(),'_ErrorLog.txt') 

    return content;

def initial_DB(db_name,coll_name,host="localhost",port=27017):
    import pymongo
    client=pymongo.MongoClient(host,port)
    db=client[db_name]
    coll=db[coll_name]
    return coll

def insert_Doc(doc,coll):
    doc_id = coll.insert(doc)
    return doc_id

def write_DB(nodeList,db_name='KTGG',coll_name='PublicInfo_Nov16'):
    coll=initial_DB(db_name,coll_name)
    for item in nodeList:
        insert_Doc(item,coll)

    return;

def convertTime(buf):
    dic={
        '一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '〇':0, '十':'',
        '年':'-', '月':'-', '日':'','零' : 0,'壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6,
        '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
    }
    return;

def writeText(tmp,filename):
    try:
        with open('E:\\Yue\\PY\\data\\'+filename, 'a+', encoding='utf-8') as f:
            f.write(str(tmp))
            f.write('\r\n')
    except:
        traceback.print_exc()
        writeText(traceback.format_exc(),'_ErrorLog.txt')

    return;

def parseLinks(class_name,tmp): # 从网页中截取sub-link, 天津 吉林
    soup=BeautifulSoup(tmp, 'html.parser')
    Links=[]
    for span in soup.find_all(class_=class_name):  # 依照class, <a href=''> 抓link
        for link in span.find_all('a'):
            Links.append(link.get('href'))
    return Links

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

# ==============================<<每日同步>>==============================
def getShanghai(): #上海高级人民法院, Normalize.py进行解析
    filename='Shanghai.txt'
    url_i="http://www.hshfy.sh.cn/shfy/gweb/ktgg_search_content.jsp?yzm=9VPw&ft=&ktrqks="\
        +time.strftime("%Y-%m-%d", time.localtime())\
        +"&ktrqjs=2017-12-31&spc=&yg=&bg=&ah=&pagesnum="

    for i in range(1,2102): #numbers of page
        url=url_i+str(i)
        tmp=getContent(url)
        writeText('\r\n['+url+']\r\n',filename)
        writeText(tmp.encode('gbk','ignore'),filename)
        time.sleep(0.5)

        print('[上海] Page ',i,' saved')

    appendix('上海',filename)
    
    return;

def getZhejiang(): #浙江, 以list格式存入txt
    filename='Zhejiang.txt'
    post={
        'pageno':1,
        'pagesize':10,
        'cbfy':'全部',
        'yg':'',
        'bg':'',
        'spz':'',
        'jarq1':'',
        'jarq2':''}

    for i in range(1,21001):
        url='http://www.zjsfgkw.cn/Notice/NoticeKTSearch'
        buf=postContent(url,post)
        soup=BeautifulSoup(buf,'html.parser')
        writeText(soup,filename)
        print('[浙江] Page ',i,' saved')

    appendix('浙江',filename)

    return;

def getJiangxi(): #江西, 以dic格式存入txt
    filename='Jiangxi.txt'

    for i in range(0,9999):
        url ='http://59.63.161.224/liti/TrialOpenCourtNotice/trialopencourtnotice!getAnnouncementAjaxp.action?jsoncallback=jQuery17106591184050880666_1467196618791&belongToCourtId=6DD3FC31043B40F286D8D4C504E70268&page.pageNo='\
            +str(i)\
            +'&page.pageSize=6&page.order=asc%2Casc&page.orderBy=openCourtDate%2Cid&_t=1467196619063&_='+str(1467196619064+i)
        buf=getContent(url)
        data = re.search(r'\{"autoCount":.+action"\}', buf).group().replace('true','True').replace('false','False')
        dic=eval(data)
        dic['网址']=url

        writeText(dic,filename)
        print('[江西] page ',i,' saved.')

        if dic['hasNext']==False:
            print('[江西] Break.')
            break

        time.sleep(0.5)
    
    appendix('江西',filename)

    return;

def getShandong(): #山东, 以dic格式存入txt
    filename='Shandong.txt'
    header=['法院','法庭','开庭日期','案由','审判长','原告/上诉人','被告/被上诉人','网址']
    exts=['0F', '0F1', '0F11', '0F12', '0F13', '0F14', '0F15', '0F16', '0F17', '0F18', '0F19', '0F1A', '0F1B', '0F2', '0F21', '0F22', '0F25', '0F26', '0F27', '0F28', '0F29', '0F2A', '0F2B', '0F2D', '0F3', '0F31', '0F32', '0F33', '0F34', '0F35', '0F36', '0F37', '0F39', '0F4', '0F41', '0F42', '0F43', '0F44', '0F45', '0F46', '0F5', '0F51', '0F52', '0F53', '0F54', '0F55', '0F56', '0F6', '0F61', '0F62', '0F63', '0F64', '0F65', '0F66', '0F67', '0F68', '0F69', '0F6A', '0F6B', '0F6C', '0F6D', '0F6E', '0F7', '0F71', '0F72', '0F73', '0F75', '0F76', '0F77', '0F78', '0F79', '0F7A', '0F7B', '0F7D', '0F7E', '0F8', '0F82', '0F83', '0F84', '0F85', '0F86', '0F87', '0F88', '0F89', '0F8A', '0F8B', '0F8C', '0F8D', '0F9', '0F91', '0F92', '0F94', '0F95', '0F96', '0F97', '0F98', '0FA', '0FA1', '0FA2', '0FA4', '0FA6', '0FB', '0FB2', '0FB3', '0FB4', '0FB5', '0FB6', '0FC', '0FC1', '0FC2', '0FC3', '0FC5', '0FC6', '0FC7', '0FC8', '0FD', '0FD3', '0FD5', '0FD6', '0FD7', '0FD8', '0FD9', '0FDC', '0FE', '0FE1', '0FE2', '0FE3', '0FE4', '0FE5', '0FE6', '0FE7', '0FE8', '0FF', '0FF1', '0FF2', '0FF4', '0FF6', '0FF7', '0FF8', '0FF9', '0FFA', '0FFB', '0FFC', '0FFD', '0FFE', '0FFF', '0FG', '0FG1', '0FG2', '0FG4', '0FG5', '0FG6', '0FG7', '0FG8', '0FG9', '0FGA', '0FH', '0FH1', '0FH2', '0FI', '0FJ', '0FJ1', '0FJ2']
    count=error=0

    for court_no in exts:
        for curPage in range(1,10):
            url='http://www.sdcourt.gov.cn/sdfy_search/tsxx/list.do?tsxx.court_no='+court_no+'&kssj_start=&kssj_end=&yg=&bg=&curPage='+str(curPage)

            soup=BeautifulSoup(getContent(url),'html.parser')
        
            for table in soup.find_all(id="tsxxTableId"):
                for row in table.find_all('tr'):
                    cells = row.find_all(re.compile('td'))

                    if len(cells)==7:
                        List=[]
                        for i in range(0,7):
                            tmp=re.sub(r'\s+','',cells[i].find(text=True))
                            List.append(tmp)

                        List.append(url)

                        dic=dict.fromkeys(header)
                        it=iter(List)
                        for k in header:
                            dic[k]=next(it)

                        writeText(dic,filename)
                        print("[山东] Page ", court_no, '-',curPage, ' has writen.')
                        count+=1
                    else:
                        error+=1
                        print('[山东] fail.')

            time.sleep(0.5)

    appendix('山东',filename)
    print("Summary(count,error): ",count,", ",error)

    return;

def getHebei(): #河北, 简化的html格式存入txt
    url_s='http://hbgy.hbsfgk.org/ktggPage.jspx?channelId=432&listsize=50000&pagego='
    filename='Hebei.txt'
    Links=[]
    for i in range(1,50000): #50000为虚拟值 实际上不会跑到
        url=url_s+str(i)
        page=getContent(url)
        Links=parseLinks('sswy_news',page)

        for fwd in Links:
            soup=BeautifulSoup(getContent(fwd),'html.parser')
            tmp=soup.find_all(class_='ywzw_con_inner')
            writeText(tmp,filename)
            writeText('\r\n['+url+']\r\n',filename)

        time.sleep(0.5)

        if re.search(r'2015-\d\d-\d\d',page): 
        # 如果本页有2015的资料, 则到此为止
            print('2015: page-',i)
            break

    appendix('河北',filename)
    return;

def getInnerMongolia(): #内蒙古, 简化的html格式存入txt(同云南)
    filename='InnerMongolia.txt'
    url_i='http://www.nmgfy.gov.cn/ktggPage.jspx?channelId=17748&listsize=171&pagego='

    tmp=getContent(url_i+'1')
    pagecount=int(re.search(r'listsize=\d+',tmp).group().replace('listsize=',''))

    for i in range(1,pagecount+1):
        url=url_i+str(i)
        Page=getContent(url)
        soup=BeautifulSoup(Page,'html.parser')
        Links=[]

        for row in soup.find_all(class_='sswy_news'):
            for ele in row.find_all('li'):
                Links.append(ele.a.get('href'))

        for link in iter(Links):
            buf=getContent(link)
            soup=BeautifulSoup(buf,'html.parser')
            tmp=soup.find_all(class_='ywzw_con_inner')[0]
            writeText(tmp,filename)
            writeText('\r\n['+url+']\r\n',filename)

        print('[内蒙古] page ',i,' saved.')

    appendix('内蒙古',filename)
    return;

def getJilin(): #吉林, 简化的html格式存入txt
    filename='Jilin.txt'
    
    for i in range(1,4):
        Links=[]
        url='http://www.jlsfy.gov.cn/ktggPage.jspx?channelId=18810&listsize=4&pagego='+str(i)
        for ele in parseLinks('organList',getContent(url)):
            Links.append(ele)

        for fwd in iter(Links):
            dic={}
            soup=BeautifulSoup(getContent(fwd), 'html.parser')

            for div in soup.find_all(class_='page'):
                dic['网址']=fwd
                dic['内容']=div
                writeText(dic,filename)

            writeText('\r\n['+fwd+']\r\n',filename)

        print('[吉林] page ',i,' saved.')

    appendix('吉林',filename)
    return;

def getGuangdong(): #广东, 简化的html格式存入txt
    filename='Guangdong.txt'
    header=[' 案号','当事人','主审法官','更新时间']
    url_i='http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?'
    
    buf=getContent(url_i)
    pagecount=re.search(r'pagecount:\s\d{4,}',buf).group().replace('pagecount: ','')
    pagecount=int(pagecount)
    print('Pagecount: ',pagecount)
    
    Links=[]
    for i in range(1,5):#pagecount+1):
        url='http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?'\
            'gglx=1&ggbt=&countNum=12&endRowNum='+str(i*12)+'&pageclickednumber='+str(i)
        buf=getContent(url)
        soup=BeautifulSoup(buf,'html.parser')

        for link in soup.find_all(class_='NewListLink'):
            tmp=re.sub(r'\s+','',link.get('href'))
            Links.append(tmp)
    
    print('Link No: ', len(Links) )

    for exts in iter(Links):
        url='http://www.gdcourts.gov.cn'+exts
        buf=getContent(url)
        soup=BeautifulSoup(buf,'html.parser')

        dic={}
        dic['网址']=url
        for cells in soup.find_all(class_='table_list_B'):
            dic['内容']=cells.find_all(True)
            writeText(dic,filename)
            # 可直接写解析逻辑
    
    appendix('广东',filename)
    return;

def getHenan(): #河南, 简化的html格式存入txt
    filename='Henan.txt'
    url_i='http://ssfw.hncourt.gov.cn/ktggPage.jspx?channelId=14631&listsize=219&pagego='

    tmp=getContent(url_i+'1')
    pagecount=int(re.search(r'listsize=\d+',tmp).group().replace('listsize=',''))

    for i in range(1,pagecount+1):
        Links=[]
        url=url_i+str(i)
        soup=BeautifulSoup(getContent(url),'html.parser')

        for row in soup.find_all(class_='list'):
            Links.append(row.a.get('href'))

        for link in iter(Links):
            soup=BeautifulSoup(getContent(link),'html.parser')
            tmp=soup.find_all(class_='list')
            writeText(tmp,filename)
            writeText('\r\n['+url+']\r\n',filename)

        print('[河南] page ',i,' saved.')

    appendix('河南',filename)
    return;

def getHubei(): #湖北, 简化的html格式存入txt
    filename='Hubei.txt'
    url="http://www.hbfy.org/gfcms/templetPro.do?templetPath=overtbegin/overtbeginPage.html"
    Court_Code={
        'H00':'湖北省高级人民法院','H80':'荆门市中级人民法院','H81':'荆门市东宝区人民法院','H82':'荆门市钟祥市人民法院',
        'H83':'荆门市京山县人民法院','H84':'荆门市沙洋县人民法院','H85':'荆门市沙洋人民法院','H86':'荆门市掇刀区人民法院',
        'HE0':'随州市中级人民法院','HE1':'随州市曾都区人民法院','HE2':'随州市广水市人民法院','HE3':'湖北省随县人民法院',
        'H60':'襄阳市中级人民法院','H61':'襄阳市樊城区人民法院','H62':'襄阳市襄城区人民法院','H63':'襄阳市老河口市人民法院',
        'H64':'襄阳市枣阳市人民法院','H65':'襄阳市襄州区人民法院','H66':'襄阳市宜城市人民法院','H67':'襄阳市南漳县人民法院',
        'H68':'襄阳市谷城县人民法院','H69':'襄阳市保康县人民法院','H6A':'襄阳市高新技术开发区人民法院','H30':'十堰市中级人民法院',
        'H31':'十堰市茅箭区人民法院','H32':'十堰市张湾区人民法院','H33':'十堰市丹江口市人民法院','H34':'十堰市郧阳区人民法院',
        'H35':'十堰市郧西县人民法院','H36':'十堰市竹山县人民法院','H37':'十堰市竹溪县人民法院','H38':'十堰市房县人民法院',
        'H5G':'神农架林区人民法院','HC0':'恩施土家族苗族自治州中级人民法院','HC1':'恩施州恩施市人民法院','HC2':'恩施州咸丰县人民法院',
        'HC3':'恩施州鹤峰县人民法院','HC4':'恩施州利川市人民法院','HC5':'恩施州建始县人民法院','HC6':'恩施州巴东县人民法院',
        'HC7':'恩施州宣恩县人民法院','HC8':'恩施州来凤县人民法院','H50':'宜昌市中级人民法院','H51':'宜昌市西陵区人民法院',
        'H52':'宜昌市伍家岗区人民法院','H53':'宜昌市点军区人民法院','H54':'宜昌市三峡坝区人民法院','H55':'宜昌市猇亭区人民法院',
        'H56':'宜昌市葛洲坝人民法院','H57':'宜昌市夷陵区人民法院','H58':'宜昌市宜都市人民法院','H59':'宜昌市枝江市人民法院',
        'H5A':'宜昌市当阳市人民法院','H5B':'宜昌市远安县人民法院','H5C':'宜昌市兴山县人民法院','H5D':'宜昌市秭归县人民法院',
        'H5E':'宜昌市长阳土家族自治县人民法院','H5F':'宜昌市五峰土家族自治县人民法院','H40':'荆州市中级人民法院','H41':'荆州市沙市区人民法院',
        'H42':'荆州市荆州区人民法院','H43':'荆州市江陵县人民法院','H44':'荆州市石首市人民法院','H45':'荆州市洪湖市人民法院',
        'H46':'荆州市松滋市人民法院','H47':'荆州市公安县人民法院','H48':'荆州市监利县人民法院','HA0':'孝感市中级人民法院',
        'HA1':'孝感市孝南区人民法院','HA2':'孝感市汉川市人民法院','HA3':'孝感市应城市人民法院','HA4':'孝感市云梦县人民法院',
        'HA5':'孝感市安陆市人民法院','HA6':'孝感市大悟县人民法院','HA7':'孝感市孝昌县人民法院','H10':'武汉市中级人民法院',
        'H11':'武汉市汉阳区人民法院','H12':'武汉市青山区人民法院','H13':'武汉市新洲区人民法院','H14':'武汉市洪山区人民法院',
        'H15':'武汉市江夏区人民法院','H16':'武汉市硚口区人民法院','H17':'武汉市江汉区人民法院','H18':'武汉市武昌区人民法院',
        'H19':'武汉市东西湖区人民法院','H1A':'武汉市江岸区人民法院','H1B':'武汉市汉南区人民法院','H1C':'武汉经济技术开发区人民法院',
        'H1D':'武汉市黄陂区人民法院','H1E':'武汉市蔡甸区人民法院','H1F':'武汉市东湖新技术开发区人民法院','HB0':'咸宁市中级人民法院',
        'HB1':'咸宁市咸安区人民法院','HB2':'咸宁市赤壁市人民法院','HB3':'咸宁市嘉鱼县人民法院','HB4':'咸宁市通城县人民法院',
        'HB5':'咸宁市崇阳县人民法院','HB6':'咸宁市通山县人民法院','H20':'黄石市中级人民法院','H21':'黄石市黄石港区人民法院',
        'H22':'黄石市西塞山区人民法院','H23':'黄石市下陆区人民法院','H24':'黄石市铁山区人民法院','H25':'黄石市大冶市人民法院',
        'H26':'黄石市阳新县人民法院','H70':'鄂州市中级人民法院','H71':'鄂州市鄂城区人民法院','H72':'鄂州市华容区人民法院',
        'H73':'鄂州市梁子湖区人民法院','H70':'鄂州市中级人民法院','H71':'鄂州市鄂城区人民法院','H72':'鄂州市华容区人民法院',
        'H73':'鄂州市梁子湖区人民法院','HD0':'湖北省汉江中级人民法院','HD1':'仙桃市人民法院','HD2':'潜江市人民法院',
        'HD3':'天门市人民法院','H90':'黄冈市中级人民法院','H91':'黄冈市黄州区人民法院','H92':'黄冈市团风县人民法院',
        'H93':'黄冈市浠水县人民法院','H94':'黄冈市蕲春县人民法院','H95':'黄冈市武穴市人民法院','H96':'黄冈市黄梅县人民法院',
        'H97':'黄冈市红安县人民法院','H98':'黄冈市罗田县人民法院','H99':'黄冈市麻城市人民法院','H9A':'黄冈市英山县人民法院'}
    post={
        'page':1,
        'currChannelid':'5913d1c6-a73b-4cec-923c-c63376a05752',
        'currUnitId':'',
        'siteid':'ce0b9496-6b88-4f66-8da7-ede1a989fd6e',
        'dsr':'',
        'pageNum':5}

    for k in Court_Code.keys():
        post['currUnitId']=k
        buf=postContent(url,post)
        tmp=re.search(r'共&nbsp;<b>\d+</b>&nbsp;页',buf).group()
        pagecount=int(re.search(r'\d+',tmp).group())
        # 获取pagecount

        for i in range(1,pagecount+1):
            post['page']=i
            soup=BeautifulSoup(postContent(url,post),'lxml')
            table=soup.find_all(class_="zebra")
            writeText(table,filename)
            print('[湖北] Page ',k,' saved.')

        break
            
    appendix('湖北',filename)

    return; #湖北
    return;

def getGuizhou(): #贵州, 简化的html格式存入txt
    filename='Guizhou.txt'
    url_i='http://www.guizhoucourt.cn/ktggPage.jspx?channelId=54&listsize=120&pagego='
    tmp=getContent(url_i+'1')
    pagecount=int(re.search(r'listsize=\d+',tmp).group().replace('listsize=',''))

    for i in range(1,pagecount+1):
        url=url_i+str(i)
        buf=getContent(url)
        Links=[]

        for fwd in parseLinks(buf,'case fl axx'): Links.append(fwd)
        for fwd in parseLinks(buf,'case fr bxx'): Links.append(fwd)

        for link in iter(Links):
            soup=BeautifulSoup(getContent(link),'html.parser')
            tmp=soup.find_all(style="min-height:400px;")
            writeText(tmp,filename)
            writeText('\r\n['+url+']\r\n',filename)

        print('[贵州] page ',i,' saved.')

    appendix('贵州',filename)
    return;

def getYunnan(): #云南, 简化的html格式存入txt
    filename='Yunnan.txt'
    url_i='http://www.ynfy.gov.cn/ktggPage.jspx?channelId=858&listsize=500&pagego='
    
    tmp=getContent(url_i+'1')
    pagecount=int(re.search(r'listsize=\d+',tmp).group().replace('listsize=',''))

    for i in range(1,pagecount+1):
        url=url_i+str(i)
        soup=BeautifulSoup(getContent(url),'html.parser')
        Links=[]

        for row in soup.find_all(class_='sswy_news'):
            for ele in row.find_all('li'):
                Links.append(ele.a.get('href'))

        for link in iter(Links):
            soup=BeautifulSoup(getContent(link),'html.parser')
            tmp=soup.find_all(class_='ywzw_con_inner')
            writeText(tmp,filename)
            writeText('\r\n['+url+']\r\n',filename)
        
        print('[云南] page ',i,' saved.')

    appendix('云南',filename)
    return;

# ==============================<<间隔同步11/16>>==============================

def getTianjin(): #天津, 抓下来未解析
    filename='Tianjin.txt'

    for i in range(1,5):
        url='http://tjfy.chinacourt.org/article/index/id/MzDIMTCwMDAwNCACAAA%3D/page/'+str(i)+'.shtml'
        buf=getContent(url)
        Links=[]
        for ele in parseLinks(buf,'left'):
            Links.append("http://tjfy.chinacourt.org"+ele)

        for fwd in iter(Links): # 从sub-link取页面回来
            writeText('\r\n['+fwd+']\r\n',filename)

            buf=getContent(fwd).replace('\xa9','')
            soup=BeautifulSoup(buf, 'html.parser')
            for div in soup.find_all(class_='text'):
                writeText(div,filename)

        print('[天津] page ',i,' saved.')

    appendix('天津',filename)
    
    # 加入写入时间

def getChongqing(): #重庆, 简化的html格式存入txt
    url_i='http://www.cqfygzfw.com/court/gg_listgg.shtml?page='
    filename='Chongqing.txt'
    buf=getContent(url_i)
    pagecount=int(re.search(r'当前1/\d+',buf).group().replace('当前1/',''))

    for i in range(1,pagecount+1):
        url=url_i+str(i)
        soup=BeautifulSoup(getContent(url),'html.parser')
        Links=[]

        for row in soup.find_all('tbody'):
            for ele in row.find_all(href="javascript:void()"):
                ids=ele.get('onclick').replace('openKtgg(\'','').replace('\')','')
                Links.append('http://www.cqfygzfw.com/court/gg_ggxx.shtml?gg.id='+ids)

        for fwd in Links:
            soup=BeautifulSoup(getContent(fwd),'html.parser')
            for content in soup.find_all('tbody'):
                writeText(content,filename)
                writeText('\r\n['+fwd+']\r\n',filename)

        print('[重庆] page ',i,' saved.')

    appendix('重庆',filename)
    
    return;

def getAnhui(): #安徽, list存入txt中
    filename='Anhui.txt'
    buf=getContent('http://www.ahgyss.cn/ktgg/index_1.jhtml')
    soup=BeautifulSoup(buf,'html.parser')
    
    for ele in soup.find_all(class_='zt_02'):
        tmp=re.sub(r'\D','',str(ele.find_all(text=True)))

    pagecount=int(tmp)

    for i in range(1,pagecount+1):
        url='http://www.ahgyss.cn/ktgg/index_'+str(i)+'.jhtml'
        buf=getContent(url)
        Links=re.findall('\"(http://www.ahgyss.cn/ktggInfo.jspx\?[\S]+?)\"',buf)

        for fwd in Links:
            result=[]
            page=re.sub('\s+','',getContent(fwd))

            try:
                t=re.search('value=\"2016-\d+-\d+',page).group().replace('value=\"','')
                court=re.search('来源:\w+?法院',page).group().replace('来源:','')
                case_no=re.search('案号：[\d\w()]+?号',page).group().replace('案号：','')
                content=re.search('\w+?开庭审理',page).group()

                result.append(fwd)
                result.append(t)
                result.append(court)
                result.append(case_no)
                result.append(content)

                print(result)

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

            writeText(result,filename)
            time.sleep(0.5)

        print('[安徽] page ',i,' saved.')

    appendix('安徽',filename)
    

    return;

def getLiaoning(): #辽宁, list存入txt中
    filename='Liaoning.txt'
    buf=getContent('http://lnfy.chinacourt.org/fyxx/more.php?LocationID=0304000000')
    pagecount=int(re.search(r'<font color="blue">\d{2,}',buf).group().replace('<font color="blue">',''))
    print('pagecount= ',pagecount)

    try:
        for i in range(5,pagecount+1):
            url='http://lnfy.chinacourt.org/fyxx/more.php?p='+str(i)+'&LocationID=0304000000'
            Links=[]
            soup=BeautifulSoup(getContent(url),'html.parser')

            for table in soup.find(class_="main_bg"):
                for ele in table.find_all('a'):
                    Links.append('http://lnfy.chinacourt.org'+ele.get('href'))

            Links.pop()
            Links.pop()

            for fwd in Links:
                sub=getContent(fwd,'gbk')
                result=[]
                result.append(fwd)
                result.append(re.search(r'发布时间：\d{4}-\d{2}-\d{2}',sub).group())
                result.append(\
                    re.search(
                        r'[：、，。（）()\w]+?案',sub).group().replace('</b>','') if re.search(r'[：、，。（）()\w]+?案',sub)!=None else ''\
                    )
                writeText(result,filename)

            print('[辽宁] page ',i,' saved.')
            time.sleep(0.5)
    except AttributeError:
        return;
    finally:
        traceback.print_exc()
        writeText(traceback.format_exc(),'_ErrorLog.txt')

    appendix('辽宁',filename)
    
    
    return;

def getHainan():#海南, list存入txt中
    filename='Hainan.txt'
    buf=getContent('http://www.hicourt.gov.cn/ggws/default.asp','gbk')
    Links=[]

    for sub in re.findall('href="(show_bulletin\.asp\?bid=[\d-]+)',buf):
        Links.append('http://www.hicourt.gov.cn/ggws/'+sub)

    for fwd in Links:
        result=[]
        page=re.sub('\s+','',getContent(fwd,'gbk'))

        try:
            t=re.search('二○一六年\w+月\w+日</p>',page).group().replace('</p>','')
            court=re.search('\w+?法院</strong>',page).group().replace('</strong>','')
            case_no=re.search('[\d\w()]+?号',page).group()
            content=re.search('[、，。○（）\w]+?一案',page).group()

            result.append(fwd)
            result.append(t)
            result.append(court)
            result.append(case_no)
            result.append(content)

            print(result)

        except AttributeError:
            print(fwd)
            traceback.print_exc()
            writeText(traceback.format_exc(),'_ErrorLog.txt')
            continue

        writeText(result,filename)
        time.sleep(0.5)

    appendix('海南',filename)
    return;

def getHunan(): #湖南, list存入txt中
    filename='Hunan.txt'
    buf=getContent('http://hunanfy.chinacourt.org/article/index/id/M0jONTAwNzAwNCACAAA%3D/page/1.shtml')
    s=re.search('\d+.shtml">尾页',buf).group()
    pagecount=int(s.split('.',1)[0])
    count=other=0

    for i in range(1,pagecount+1):
        url='http://hunanfy.chinacourt.org/article/index/id/M0jONTAwNzAwNCACAAA%3D/page/'+str(i)+'.shtml'
        soup=BeautifulSoup(buf,'html.parser')
        Links=[]

        for tag in soup.find_all(class_="font14"):
            for link in tag.find_all(target='_blank'):
                sub=link.get('href')
                if re.match('/article/detail/[\w/]+.shtml',sub)!=None:
                    Links.append('http://hunanfy.chinacourt.org'+sub)
                    count+=1
                    # 符合子网页的链结格式
                else:
                    other+=1
                    continue

        print('Summary(match,none)=', count, ',', other)

        for fwd in Links:
            page=getContent(fwd)
            soup=BeautifulSoup(page,'html.parser')
            result=[]

            try:
                result.append(fwd)
                result.append(re.search('发布时间：[\d-]+',page).group())
                result.append(soup.find_all(class_='detail_bigtitle')[0].string)

                div=str(soup.find_all('div', class_='detail_txt detail_general'))
                content=re.sub('<.+>','',div)
                content=re.sub('\s+','',content)
                result.append(content) 
                # 去除内容中多余的符号跟空白

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

            writeText(result,filename)

        print('[湖南] page ',i,' saved.')

    appendix('湖南',filename)
    

    return;

def getGansu(): #甘肃, list存入txt中
    filename='Gansu.txt'

    for i in range(1,5000):
        Links=[]
        buf=getContent('http://gsgf.gssfgk.com/ktggPage.jspx?channelId=307&listsize=3695&pagego='+str(i))
        soup=BeautifulSoup(buf,'html.parser')

        for ele in soup.find_all(style='display:block; height:620px;  width:700px;'):
            for li in ele.find_all('li'):
                sub=li.a.get('href')
                Links.append(sub)

        for fwd in Links:
            result=[]
            page=getContent(fwd)

            t=re.search('时间：[\d-]+',page).group()
            court=re.search('作者：\w+',page).group()
            content=re.search('2em;">[\w\s]+',page).group().replace('2em;">','')

            result.append(fwd)
            result.append(t)
            result.append(court)
            result.append(content)

            print(result)

            writeText(result,filename)
            time.sleep(0.5)

        print('[甘肃] page ',i,' saved.')

        if re.search(r'2015-\d\d-\d\d',buf): # 如果本页有2015的资料, 则到此为止
            print('2015: page-',i)
            break

    appendix('甘肃',filename)
    

    return;

def getNingxia(): #宁夏, list存入txt中
    filename='Ningxia.txt'

    for i in range(2,100):
        Links=[]
        url='http://www.nxfy.gov.cn/sfgk/ktgg/index.html' if i==0 else 'http://www.nxfy.gov.cn/sfgk/ktgg/index_'+str(i)+'.html'
        buf=getContent(url,'gbk')

        for ele in re.findall('<a href=".(\/201[\s\S]+?)" target="_blank">',buf):
            Links.append('http://www.nxfy.gov.cn/sfgk/ktgg'+ele)
            # 产生完整的url

        for fwd in Links:
            result=[]
            page=re.sub('\s+','',getContent(fwd,'gbk'))

            try:
                t=re.search('二〇一\w年\w+月\w+日{0,1}',page).group()
                court=re.search('TRS_Editor>.+?法院',page).group()
                court=re.search('\w+?法院',court).group()
                content=re.search('[：、，。（）()\w]+?一案',page).group()

                result.append(fwd)
                result.append(t)
                result.append(court)
                result.append(content)

                print(result)

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

            writeText(result,filename)
            time.sleep(0.5)

        print('[宁夏] Page ',i,' saved.')

        if re.search(r'2015年\d+月\d+日',buf): # 如果本页有2015的资料, 则到此为止
            print('[终止] 2016 end.')
            break

    appendix('宁夏',filename)
    

    return;

def getQinhai(): #青海, list存入txt中
    filename='Qinhai.txt'
    url_i='http://www.qhcourt.gov.cn/ktggPage.jspx?channelId=448&listsize=5018&pagego='
    header=['网址','发布时间','法院','公告正文']

    for i in range(1,5018):
        url=url_i+str(i)
        buf=getContent(url)
        Links=re.findall('<li><a href="([\s\S]+?)" title=',buf)

        for fwd in Links:
            result=[]
            page=re.sub('\s+','',getContent(fwd))

            try:
                t=re.search('2016-\d+-\d+</p>',page).group().replace('</p>','')
                court=re.search('\w+?法院</h3>',page).group().replace('</h3>','')
                content=re.search('[：、，。（）()\w]+?一案',page).group()

                result.append(fwd)
                result.append(t)
                result.append(court)
                result.append(content)

                dic=createDict('青海法院审判信息网',header,result)
                print(result)

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

            writeText(dic,filename)
            time.sleep(0.5)

        print('[青海] Page ',i,' saved.')

        if re.search(r'2015-\d+-\d+',buf): # 如果本页有2015的资料, 则到此为止
            print('[青海] End at page ',i,'.')
            break

    appendix('青海',filename)
    

    return;

def getFujian(): #福建, dic->DB
    header=['省级行政区','网址','内容','时间','法院']
    url='http://www.fjcourt.gov.cn/page/public/courtreport.html?'
    post={
        '__VIEWSTATE':'',
        '__EVENTTARGET':'ctl00$cplContent$AspNetPager1',
        '__EVENTARGUMENT':1}
    vs=''

    for i in range(1,300):
        post['__VIEWSTATE']=vs
        post['__EVENTARGUMENT']=i

        Links=[]
        result=[]
        buf=postContent(url,post)
        vs=re.findall('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*)?"', buf)[0]
        #找到新的viewstate

        for ele in re.findall('<li><a href="(\/Page\/Court\/News\/Announcement.aspx\?ajbs=\d+?)"',buf):
            Links.append('http://www.fjcourt.gov.cn'+ele)

        for fwd in Links:
            node=node.fromkeys(header)
            page=re.sub('\s+','',getContent(fwd))
            
            try:
                node['省级行政区']='福建省'
                node['网址']=fwd
                node['时间']=re.search('二〇一六年\w+月\w+日',page).group()
                node['法院']=re.findall('<spanclass=\'article-author\'>(\w+?法院)',page)[0] #注意! re.findall为list
                node['标题']=re.search('[：、，。（）()\w]+?开庭公告',page).group()
                node['内容']=re.search('[：、，。（）()\w]+?特此公告',page).group()

                result.append(node)
                print(result)

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

        write_DB(result)            
        print('[福建] Page ',i,' saved.')

        if re.search('\[2015-\d+-\d+\]',buf): # 如果本页有2015的资料, 则到此为止
            print('[福建] End at page ',i,'.')
            break

    return;

def getBeijing(): #北京, dic->DB, 有验证码
    filename='Beijing.txt'
    url_i='http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p='
    header=['省级行政区','网址','内容','时间','法院']
    flag=True

    for i in range(1,7000):
        url=url_i+str(i)
        buf=getContent(url)
        Links=[]
        

        for ele in re.findall('<a href="(/ktgg/ktggDetailInfo.htm?[\s\S]+?)"',buf):
                Links.append('http://www.bjcourt.gov.cn'+ele)

        for fwd in Links:
            result=[]
            page=re.sub('\s+','',getContent(fwd))

            if re.search('定于二〇一五年',page): # 如果本页有2015的资料, 则到此为止
                print('[北京] 2016 end.')
                flag=False
                break
            elif re.search('验证码',page):
                print('[北京] ',fwd)
                print('[北京] 验证码,等待90秒后重试.')
                time.sleep(90)

            try:
                t=re.search('二〇一六年\w+月\w+日',page).group()
                court=re.search('来源:\w+?法院',page).group().replace('来源:','')
                content=re.search('[：、，。.（）()\w]+?一案',page).group()
                
                result.append('北京市')
                result.append(fwd)
                result.append(t)
                result.append(court)
                result.append(content)

                print(result)

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

        if flag==False:
            print('[北京] End at page ',i,'.')
            break
        else:
            writeText(result,filename)
            #write_DB(result)
            print('[北京] Page ',i,' saved.')
    
    return;

# ==============================<<Instance>>==============================


with open('E:\Yue\PY\Final\MajorCrawler.py','r',encoding='utf8') as f:
    l=re.findall('get(\w+?)\(\):',f.read())
    print('Current crawlers: ',len(l))
