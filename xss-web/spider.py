
from selenium import webdriver

from bs4 import BeautifulSoup

import random 

import re

import time

import mysql.connector

import xlwt

#初始化火狐浏览器

def init(url):

    firefox_login=webdriver.Firefox()

    firefox_login.get(url)

    firefox_login.maximize_window()

    return firefox_login

# 登录淘宝并进行商品搜索  

def login(firefox_login):

    firefox_login.find_element_by_id('J_Quick2Static').click()

    firefox_login.find_element_by_id('TPL_username_1').clear()

    firefox_login.find_element_by_id('TPL_username_1').send_keys(u'荆棘里的蜥蜴')

    firefox_login.find_element_by_id('TPL_password_1').clear()

    firefox_login.find_element_by_id('TPL_password_1').send_keys(u'chaochao00..')

    a=firefox_login.find_element_by_id('J_SubmitStatic')   

    a.click()

    time.sleep(random.randint(6,8))

    firefox_login.find_element_by_id('q').clear()

    firefox_login.find_element_by_id('q').send_keys(u'魅族mx6')   

    firefox_login.find_element_by_class_name("btn-search").click() 

    time.sleep(random.randint(5,8))

    firefox_login.find_element_by_xpath('//a[@traceidx="0"]').click() 

    """

    time.sleep(10)

    js="var q=document.documentElement.scrollTop=10000"

    firefox_login.execute_script(js)

    time.sleep(10)

    b=firefox_login.find_element_by_xpath('//a[@data-index="2"]')

    b.click()

    """

    return firefox_login

#得到总的页面数目    

def get_pageNum(firefox_login):

    data=firefox_login.page_source

    soup=BeautifulSoup(data,'lxml')

    comments=soup.find("div", class_="total")  #匹配总的页数

    pattern=re.compile(r'[0-9]+')

    pageNum=re.search(pattern,comments.text).group(0)  # 将数字页数提取

    pageNum=int(pageNum)

    return pageNum     #用于循环的次数设置

#获取每个页面的商品信息

def ObtainHtml(firefox_login):  

    js="var q=document.documentElement.scrollTop=1000"

    firefox_login.execute_script(js)

    time.sleep(2)

    js="var q=document.documentElement.scrollTop=2000"

    firefox_login.execute_script(js) 

    time.sleep(2)

    js="var q=document.documentElement.scrollTop=3000"

    firefox_login.execute_script(js) 

    time.sleep(2)  

    js="var q=document.documentElement.scrollTop=4000"

    firefox_login.execute_script(js)

    time.sleep(2)

    js="var q=document.documentElement.scrollTop=5000"

    firefox_login.execute_script(js)

    time.sleep(2)

    js="var q=document.documentElement.scrollTop=6000"

    firefox_login.execute_script(js)

    time.sleep(2)

    js="var q=document.documentElement.scrollTop=7000"

    firefox_login.execute_script(js)

    time.sleep(2)

    data=firefox_login.page_source

    soup = BeautifulSoup(data,'lxml') 

    comment=soup.find_all("div", class_="item g-clearfix")

    j=0

    for i in  comment:

        j+=1

        print(j)

        temp=[]

        Item=i.find("a",class_="J_U2IStat")  #商品详情页链接

        if Item:

            temp.append(Item.get('href'))

        shop=i.find("a",class_="shopname")

        if shop:        

            temp.append(shop.text)    #店铺名称

        address=i.find('div',class_='location') 

        if address:        

            temp.append(address.text.strip())   #店铺所在地

        priceandnum=i.find("div",class_="price-row")

        if priceandnum:        

            Y=priceandnum.find('span',class_='price g_price g_price-highlight')

            if Y:        

                temp.append(Y.text.strip('<span>'.strip('</span>').strip('<strong>').strip('</strong>').strip())) #商品价格

        Num=i.find('p',class_='col deal-cnt')

        if Num:        

            temp.append(Num.text.strip())   #购买人数

        print(temp)

        Infolist.append(temp)

            

# 点击下一页 //更新数据。   

def NextPage(firefox_login):

    firefox_login.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()  #点击下一页ajax刷新数据

    

 

#数据库连接函数    

def connDB():

    conn=mysql.connector.connect(user='root',passwd='123456',database='review',charset='utf8')

    cursor=conn.cursor()

    return(conn,cursor)

 

#关闭数据库连接

def exitConn(conn,cursor):

    cursor.close()

    conn.close()

    

#将爬取的内容保存到数据库

def SaveMySql(datalist):

    conn,cursor=connDB()

    cursor.execute('create table taoBao_mx6\

    (prod_url varchar(100),\

     store varchar(20),\

     location varchar(10),\

     price varchar(10),\

     buyer_Num varchar(10))')

     

    for i in range(0,len(Infolist)):

        data=datalist[i]

        print('insert into taoBao_mx6 values\

         (%s,%s,%s,%s,%s)',[data[0],data[1],data[2],data[3],data[4]])

        cursor.execute('insert into taoBao_mx6 values\

         (%s,%s,%s,%s,%s)',[data[0],data[1],data[2],data[3],data[4]])

        conn.commit()

    exitConn(conn,cursor)

 

#保存成excel格式的文件

def saveData(datalist,savepath):

    book=xlwt.Workbook(encoding='utf-8',style_compression=0)

    sheet=book.add_sheet(u'魅族mx6',cell_overwrite_ok=True)

    col=[u'链接',u'店名',u'地点',u'价格',u'购买人数']

    for i in range(0,5):

        sheet.write(0,i,col[i])

    for i in range(len(Infolist)):

        data=datalist[i]

        for j in range(5):

            sheet.write(i+1,j,data[j])

    book.save(savepath)

 

if __name__=='__main__':

    Infolist=[]

    url='https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'

    firefox_login=init(url)

    firefox_login=login(firefox_login)

    time.sleep(random.randint(5,6))

    Num=get_pageNum(firefox_login)

    print(Num)

    for i in range(Num-1):

        ObtainHtml(firefox_login)

        time.sleep(random.randint(2,3))

        NextPage(firefox_login)

    print("信息爬取完成")

    SaveMySql(Infolist)

    savepath='魅族mx6.xls'

    saveData(Infolist,savepath)

    firefox_login.quit()
