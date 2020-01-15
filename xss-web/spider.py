import time,re,os
from selenium import webdriver

driver = webdriver.Chrome()#获得浏览器驱动


def get_one_review(page):#获取单个页面所有影评函数
    driver.get('https://movie.douban.com/subject/25986662/reviews?start={}'.format(page))#打开目标网页
    time.sleep(2)

    t0 = time.time()#程序启动计时器
    def save_yp():
        #获得影评正文
        yp = driver.find_element_by_id('link-report').find_elements_by_tag_name('p')
        #保存正文到文件中
        names = driver.find_element_by_class_name('article').find_element_by_tag_name('h1').text#获得文件名
        name  = re.sub('[\/:*?"<>|]','-',names)#去除非法字符
        print('正在保存《{}》... ...'.format(name))#实时输出保存进度
        with open('{}.txt'.format(name),'w',encoding = 'utf-8') as f:#以文章名作为文件名进行保存
            for each in yp:
                f.write(str(each.text) + '\n')


    bt = driver.find_elements_by_class_name('main-bd')#获取本页面的20个标题
    i=0
    while i < len(bt):
        t1 = time.time()#保存单个文件的起始计时器
        link = driver.find_element_by_link_text(bt[i].find_element_by_tag_name('h2').text).click()#获取影评的链接并点击
        save_yp()#保存文件到桌面
        i += 1#计数器加1
        #下面两步必须执行，否则无法循环下载本页面的所有影评
        driver.get('https://movie.douban.com/subject/25986662/reviews?start={}'.format(page))#打开目标网页
        bt = driver.find_elements_by_class_name('main-bd')#获取本页面的20个标题
        t2 = time.time()#保存单个文件的终止计时器
        print('第{}个文件抓取共耗时{}秒'.format(i,(t2-t1)) + '\n')
    t3 = time.time()
    print('共保存了{}文件，共用时{}秒'.format(len(bt),(t3-t0)))




def get_all_review():#获取前100条评论（如果网速够好，时间够多可以选择把所有的影评都下载下来）
    for page in range(0,100,20):
        print(str(page))
        ts1 = time.time()
        get_one_review(page)
        te1 = time.time()
        print('获取本页20条评论共耗时{}秒'.format(te1-ts1))

        


if __name__ == '__main__':
    os.makedirs(r'd:\aaa')#创建路径
    os.chdir(r'd:\aaa')#将生成的文件保存在刚刚生成的文件夹内
    ts = time.time()
    get_all_review()
    te = time.time()
    print('获取100条评论共耗时{}秒'.format(te-ts))
 