from MajorCrawler import *

# ==============================<<func>>==============================

def getBJ(): #北京, dic->DB, 有验证码
    url_i='http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p='
    header=['省级行政区','网址','内容']
    flag=True

    for i in range(1,10):

        #url=url_i+str(i)
        #buf=getContent(url)
        Links=[]
        result=[]

        """
        for ele in re.findall('<a href="(/ktgg/ktggDetailInfo.htm?[\s\S]+?)"',buf):
                Links.append('http://www.bjcourt.gov.cn'+ele)
        """
        
        Links=['http://www.bjcourt.gov.cn/ktgg/ktggDetailInfo.htm?NId=58109&NAjbh=8755026']

        for fwd in Links:
            node={}
            node=node.fromkeys(header)
            page=getContent(fwd)
            soup=BeautifulSoup(page,'html.parser')

            """
            if re.search('定于二〇一五年',page): # 如果本页有2015的资料, 则到此为止
                print('[北京] 2016 end.')
                flag=False
                break
            elif re.search('验证码',page):
                print('[北京] ',fwd)
                print('[北京] 验证码,等待90秒后重试.')
                time.sleep(90)
			"""

            try:
                node['省级行政区']='北京市'
                node['网址']=fwd
                #node['内容']=

                for x in soup.find_all(class_='article_con'):
                	writeText(x,'test.txt')
                else:
                	print('class failed')
                
                result.append(node)
                print(node)

            except AttributeError:
                print(fwd)
                traceback.print_exc()
                writeText(traceback.format_exc(),'_ErrorLog.txt')
                continue

        if flag==False:
            print('[北京] End at page ',i,'.')
            break
        else:
            #write_DB(result)
            print('[北京] Page ',i,' saved.')


        break
    
    return;


# ==============================<<Main>>==============================
getBJ()